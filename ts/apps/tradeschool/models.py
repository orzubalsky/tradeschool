from django.conf import settings
from django.db.models import *
from django.contrib.localflavor.us.models import USStateField
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
#from django_mailer import send_mail
from django.template import loader, Context
from django.template import Template
from django_countries import CountryField
from tinymce.models import HTMLField
import pytz, uuid, random, time, shutil, errno, os
from datetime import *
from tradeschool.utils import copy_model_instance
from tradeschool.widgets import *



class Base(Model):
    """Base model for all of the models in the tradeschool application."""
    
    class Meta:
        abstract = True
                    
    created     = DateTimeField(auto_now_add=True, editable=False)
    updated     = DateTimeField(auto_now=True, editable=False)
    is_active   = BooleanField(default=1)

    def __unicode__ (self):
        if hasattr(self, "title") and self.title:
            return self.title
        else:
            return "%s" % (type(self))


class Email(Base):
    """Abstract model for all email notifications in the ts system.
    TS-wide notification templates, individulal branch notification templates,
    and schedule-specific notification templates extend this model."""
    
    class Meta:
        abstract = True

    EMAIL_CHOICES = (
        ('disabled', 'Disabled'),
        ('not_sent', 'Not Sent Yet'),
        ('sent', 'Sent')
    )

    subject      = CharField(max_length=140)
    content      = TextField()
    email_status = CharField(max_length=30, choices=EMAIL_CHOICES, default='not_sent')

    def preview(self, schedule_obj, registration=None):
        template = Template(self.content)
        context  = self.template_context(schedule_obj)
        body     = template.render(context)
        return body

    def send(self, schedule_obj, recipient, registration=None):
        body    = self.preview(schedule_obj)
        branch  = schedule_obj.course.branch.all()[0]
        send_mail(self.subject, body, branch.email, recipient)
        self.email_status = 'sent'
        self.save()

    def template_context(self, schedule_obj, registration=None):
        """ """
        
        teacher = schedule_obj.course.teacher
        site    = Site.objects.get_current()
        branch  = Branch.objects.get(pk=schedule_obj.course.branch.all()[0].pk)
        venue   = schedule_obj.venue
        domain  = site.domain

        student_feedback_url = "%s%s" % (domain, reverse('schedule-feedback', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug, 'feedback_type': 'student'}))
        teacher_feedback_url = "%s%s" % (domain, reverse('schedule-feedback', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug, 'feedback_type': 'teacher'}))
        class_edit_url       = "%s%s" % (domain, reverse('schedule-edit', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug,}))
        homepage_url         = "%s%s" % (domain, reverse('schedule-list', kwargs={'branch_slug': branch.slug}))

        student_list = ""
        for registration in schedule_obj.registration_set.all():
            student_list += "\n%s: " % registration.student.fullname
            student_items = []
            for item in registration.items.all():
                student_items.append(item.title)
            student_list += ", ".join(map(str, student_items))

        c = Context({
            'schedule'              : schedule_obj,
            'branch'                : branch,
            'teacher'               : teacher,
            'venue'                 : venue,
            'student_feedback_url'  : student_feedback_url,
            'teacher_feedback_url'  : teacher_feedback_url,
            'class_edit_url'        : class_edit_url,
            'homepage_url'          : homepage_url,
            'student_list'          : student_list
        })

        if registration != None:
            unregister_url = "%s%s" % (domain, reverse('schedule-unregister', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug, 'student_slug': registration.student.slug}))
            item_list = ""
            for item in registration.items.all():
                item_list += "%s\n" % item.title

            c.dicts.append({
                'student'       : registration.student,
                'registration'  : registration,
                'unregister_url': unregister_url,
                'item_list'     : item_list
            })

        return c

    def __unicode__ (self):
        return self.subject


class TimedEmail(Email):
    """
    Abstract model for all email notifications in the ts system.
    TS-wide notification templates, individulal branch notification templates,
    and course-specific notification templates extend this model. 
    """
    class Meta:
        abstract = True

    send_on      = DateTimeField(blank=True, null=True)
    days_delta   = IntegerField(default=-1)
    send_time    = TimeField(default=time(10,0,0))

    def set_send_on(self, event_datetime):
        # construct a datetime object after adding / subtracting the days delta
        send_datetime = event_datetime + timedelta(days=self.days_delta)

        # create a naive date from send_datetime
        send_date = date(send_datetime.year, send_datetime.month, send_datetime.day)

        # combine the date to send the email with the time set in the email object
        send_on_datetime = datetime.combine(send_date, self.send_time)

        # now do timezone conversion
        current_tz = timezone.get_current_timezone()
        localized_datetime = current_tz.localize(send_on_datetime)
        utc = pytz.timezone('UTC')
        normalized_datetime = utc.normalize(localized_datetime.astimezone(utc))

        # set send_on to normalized datetime
        self.send_on = normalized_datetime


class StudentConfirmation(Email):
    """An email that is sent when a student registered to a scheduled class."""
    pass


class StudentReminder(TimedEmail):
    """An email that is sent to a registered student a day before a class is scheduled to start."""
    def save(self, *args, **kwargs):
        self.days_delta = -1
        self.send_time = time(10,0,0)
        super(StudentReminder, self).save(*args, **kwargs)


class StudentFeedback(TimedEmail):
    """An email that is sent to a student a day after a scheduled class took place."""

    def save(self, *args, **kwargs):
        self.days_delta = 1
        self.send_time = time(16,0,0)
        super(StudentFeedback, self).save(*args, **kwargs)


class TeacherConfirmation(Email):
    """An email that is sent when a teacher submitted a class."""
    pass


class TeacherClassApproval(Email):
    """An email that is sent when an admin approved a teacher submitted a class."""
    pass                                 


class TeacherReminder(TimedEmail):
    """An email that is sent to a teacher a day before their class takes place."""
    
    def save(self, *args, **kwargs):
        self.days_delta = -1
        self.send_time = time(18,0,0)
        super(TeacherReminder, self).save(*args, **kwargs)


class TeacherFeedback(TimedEmail):
    """An email that is sent to a teacher a day after a scheduled class took place."""

    def save(self, *args, **kwargs):
        self.days_delta = 1
        self.send_time = time(18,0,0)
        super(TeacherFeedback, self).save(*args, **kwargs)


class EmailContainer(Base):
    """
    """
    class Meta:
        abstract = True

    student_confirmation   = ForeignKey(StudentConfirmation)
    student_reminder       = ForeignKey(StudentReminder)
    student_feedback       = ForeignKey(StudentFeedback)
    teacher_confirmation   = ForeignKey(TeacherConfirmation)
    teacher_class_approval = ForeignKey(TeacherClassApproval)
    teacher_reminder       = ForeignKey(TeacherReminder)
    teacher_feedback       = ForeignKey(TeacherFeedback)

    def emails():
        def fget(self):
            return {"student_confirmation"   : self.student_confirmation, 
                    "student_reminder"       : self.student_reminder, 
                    "student_feedback"       : self.student_feedback,
                    "teacher_confirmation"   : self.teacher_confirmation, 
                    "teacher_class_approval" : self.teacher_class_approval, 
                    "teacher_reminder"       : self.teacher_reminder, 
                    "teacher_feedback"       : self.teacher_feedback
                    }
        return locals()

    emails = property(**emails())


class DefaultEmailContainer(EmailContainer):
    """
    """

class Location(Base):
    """
    Abstract for location based models: branch & venue.     
    """
    class Meta:
        abstract = True

    title   = CharField(max_length=100, help_text="The name of the space")
    phone   = CharField(max_length=20, blank=True, null=True, help_text="Optional.")
    city    = CharField(max_length=100)
    state   = USStateField(null=True, blank=True, verbose_name="State", help_text="If in the US.")
    country = CountryField()


class BranchEmailContainer(EmailContainer):
    """
    """        
    class Meta:
        verbose_name = "Branch Emails"
        verbose_name_plural = "Branch Emails"

    branch = OneToOneField("Branch", related_name="emails")

    def __unicode__ (self):
        return u"for %s" % self.branch.title


class Cluster(Base):
    """Branches can be grouped together for possibly displaying them together on the website.
        For example: multiple branches in one city can belong to the same group."""
        
    name = CharField(max_length=100) 
    
    

class Branch(Location):
    """
    A branch is a ts organization in a specific location (usually city/region).
    The branch slug should be used to point to the individual branch app functionality.
    All dates and times in the branch's view templates should reflect the branch's timezone.   
    """    
    
    class Meta:
        verbose_name_plural = 'Branches'
        ordering = ['title']
        
    COMMON_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    
    slug        = SlugField(max_length=120, help_text="This is the part that comes after 'http://tradeschool.coop/' in the URL")
    email       = EmailField(max_length=100)
    timezone    = CharField(max_length=100, choices=COMMON_TIMEZONE_CHOICES)
    language    = CharField(max_length=50, choices=settings.LANGUAGES, null=True)
    organizers  = ManyToManyField(User)
    site        = ForeignKey(Site)
    cluster     = ForeignKey(Cluster, null=True)
    header_copy = HTMLField(null=True, blank=True, default="Barter for knowledge")
    intro_copy  = HTMLField(null=True, blank=True)
    footer_copy = HTMLField(null=True, blank=True)

    objects   = Manager()
    on_site   = CurrentSiteManager()

    
    def save(self, *args, **kwargs):
        """Check to see if the slug field's value has been changed. 
        If it has, rename the branch's template dir name."""
        
        if self.pk is not None:
            original = Branch.objects.get(pk=self.pk)
            if original.slug != self.slug:
                self.update_template_dir(original.slug, self.slug)
        super(Branch, self).save(*args, **kwargs)        
        

    def populate_notifications(self):
        "resets branch notification templates from the global branch notification templates"
                
        # delete existing branch emails
        branch_emails = BranchEmailContainer.objects.filter(branch=self).delete()
            
        # copy branch notification from the branch notification templates
        default_email_container = DefaultEmailContainer.objects.all()[0]
        
        branch_email_container = BranchEmailContainer(branch=self)
        
        for fieldname, email_obj in default_email_container.emails.iteritems():
            new_email = copy_model_instance(email_obj)
            new_email.save()
            setattr(branch_email_container, fieldname, new_email)
        branch_email_container.save()
    

    def generate_files(self):
        """ Create a directory in the templates directory for the branch.
            Make a copy of all default template files.
            Create a css and javascript file for the branch."""
        src = settings.DEFAULT_BRANCH_TEMPLATE_DIR
        dst = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.slug)
        
        try:
            shutil.copytree(src, dst)
        except OSError as exc: # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise


    def delete_files(self):
        """Delete the branch's template directory with all of the files."""
        directory = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.slug)
        
        if os.path.exists(directory):
            shutil.rmtree(directory)        

    
    def update_template_dir(self, old_dirname, new_dirname):
        """ Rename the branch's template directory name.
            Call this method after the branch's slug field has changed."""
    
        old_dirname = os.path.join(settings.BRANCH_TEMPLATE_DIR, old_dirname)
        new_dirname = os.path.join(settings.BRANCH_TEMPLATE_DIR, new_dirname)
    
        os.rename(old_dirname, new_dirname)
        

class Venue(Location):
    """Branches have venues in which scheduled classes take place."""

    TYPE_CHOICES = ((0, 'Normal'), (1, 'Alternative'))

    def random_color():
        colorValue = random.randint(0, 16777215)
        return "#%x" % colorValue

    venue_type  = SmallIntegerField(max_length=1, choices=TYPE_CHOICES, default=0)
    address_1   = CharField(max_length=50, verbose_name="Street")
    address_2   = CharField(max_length=100, blank=True, null=True)
    capacity    = SmallIntegerField(max_length=4, default=20, help_text="How many people fit in the space?")     
    resources   = TextField(null=True, default="Chairs, Tables", help_text="What resources are available at the space?")
    color       = CharField(max_length=7, default=random_color)
    branch      = ForeignKey(Branch, help_text="What tradeschool is this object related to?")


class PersonManager(Manager):
    def get_query_set(self):
        return super(PersonManager, self).get_query_set().annotate(
            registration_count  =Count('registrations', distinct=True), 
            courses_taught_count=Count('courses_taught', distinct=True)
        )


class Person(Base):
    """
    Person in the tradeschool system is either a teacher or a student.
    A person submitting a class as a teacher will have to supply a bio as well.
    """
    
    class Meta:
        verbose_name_plural = "People"
        permissions = (
            ('view_object', 'View object'),
        )        
            
    fullname    = CharField(max_length=100, verbose_name="your name", help_text="This will appear on the site.")
    email       = EmailField(max_length=100, verbose_name="Email address", help_text="Used only for us to contact you.")
    phone       = CharField(max_length=20, blank=True, null=True, verbose_name="Cell phone number", help_text="Optional. Used only for us to contact you.")
    bio         = TextField(blank=True, verbose_name="A few sentences about you", help_text="For prospective students to see on the website")
    website     = URLField(max_length=200, blank=True, null=True, verbose_name="Your website / blog URL", help_text="Optional.")
    slug        = SlugField(max_length=120, verbose_name="URL Slug", help_text="This will be used to create a unique URL for each person in TS.")
    branch      = ManyToManyField(Branch, help_text="What tradeschool is this object related to?")
    
    objects = Manager()

    def __unicode__ (self):
        return self.fullname
            

class TeacherManager(PersonManager):
    def get_query_set(self):
        return super(TeacherManager, self).get_query_set().filter(courses_taught_count__gt=0)


class Teacher(Person):
    class Meta:
        proxy = True
        
    objects = TeacherManager()


class StudentManager(PersonManager):
    def get_query_set(self):
        return super(StudentManager, self).get_query_set().filter(registration_count__gt=0)


class Student(Person):
    class Meta:
        proxy = True
 
    objects = StudentManager()
 
            
class Course(Base):
    """
    The Course class
    """

    class Meta:
        # Translators: Any times that the word class is shown as singular
        verbose_name = _("Class")
        # Translators: Any times that the word class is shown as plural
        verbose_name_plural = _("Classes")

    CATEGORIES = (
        (0, 'Arts'),
        (1, 'Etc'),
        (2, 'Food'),
        (3, 'Info'),
        (4, 'Lit'),
        (5, 'Music'),
        (6, 'Org')
    )

    teacher         = ForeignKey(Person, related_name='courses_taught')
    category        = SmallIntegerField(max_length=1, choices=CATEGORIES, default=random.randint(0, 6))    
    max_students    = IntegerField(max_length=4, verbose_name="Maximum number of students in your class")
    title           = CharField(max_length=140, verbose_name="class title") 
    slug            = SlugField(max_length=120,blank=False, null=True, verbose_name="URL Slug")
    description     = TextField(blank=False, verbose_name="Class description")
    branch          = ManyToManyField(Branch, help_text="What tradeschool is this object related to?")


class Durational(Base):
    """
    Durational is an abstract model for any model that has a start time and an end time.
    In the tradeschool system, these would be the Time and Course models.
    """
    class Meta:
		abstract = True

    start_time  = DateTimeField(default=datetime.now())
    end_time    = DateTimeField(default=datetime.now())
    
    
class Time(Durational):
    """
    Time is an open time slot. It is implemented in the frontend alone:
    These slots populate the calendar for teachers submitting a class.
    Times do not affect the admin class schedluing logic.
    """
    
    class Meta:
        verbose_name        = "Time Slot"
        verbose_name_plural = "Time Slots"
    
    venue = ForeignKey(Venue, null=True, blank=True, help_text="Is this time slot associated with a specific venue?")
    branch = ForeignKey(Branch, help_text="What tradeschool is this object related to?")

    def __unicode__ (self):
        return u"%s" % self.start_time


class TimeRange(Base):
    """
    """
    class Meta:
        verbose_name        = "Time Slot Range"
        verbose_name_plural = "Time Slot Ranges"

    start_date  = DateField(default=datetime.now())
    end_date    = DateField(default=datetime.now())
    start_time  = TimeField(default=datetime(2008, 1, 31, 18, 00, 00))
    end_time    = TimeField(default=datetime(2008, 1, 31, 19, 30, 00))
    sunday      = BooleanField()
    monday      = BooleanField()
    tuesday     = BooleanField()
    wednesday   = BooleanField()
    thursday    = BooleanField()
    friday      = BooleanField()
    saturday    = BooleanField()
    
    branch      = ForeignKey(Branch, help_text="What tradeschool is this object related to?")
        

class ScheduleEmailContainer(EmailContainer):
    """
    """
    class Meta:
        verbose_name = "Schedule Emails"
        verbose_name_plural = "Schedule Emails"

    schedule = OneToOneField("Schedule", related_name="emails")

    def email_teacher(self, email):
        """shortcut method to send an email via the ScheduleEmailContainer object."""
        return email.send(self.schedule, (self.schedule.course.teacher.email,))

    def email_student(self, email, registration):
        """shortcut method to send an email via the ScheduleEmailContainer object."""
        return email.send(self.schedule, (registration.student.email,), registration)

    def email_students(self, email):
        """shortcut method to send an email via the ScheduleEmailContainer object."""
        for registration in self.schedule.registration_set.all():
            if registration.registration_status == 'registered':
                self.email_student(email, registration)

    def preview(self, email):
        """shortcut method to preview an email via the ScheduleEmailContainer object."""
        return email.preview(self.schedule)

    def __unicode__ (self):
        return u"for %s" % self.schedule.course.title


class BarterItem(Base):
    """
    Barter items are the items that teachers request for a class they're teaching.
    The items themselves can be requested in various classes.
    """

    title = CharField(max_length=255)

    def __unicode__ (self):
        registered_count = RegisteredItem.objects.filter(barter_item=self).count()
        return u"%s (%i are bringing)" % (self.title, registered_count)


class ScheduleManager(Manager):
   def get_query_set(self):
      return super(ScheduleManager, self).get_query_set().annotate(registered_students=Count('students')).prefetch_related('course')


class SchedulePublicManager(ScheduleManager):
    def get_query_set(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        return super(SchedulePublicManager, self).get_query_set().filter(end_time__gte=now, course__is_active=1, course_status=3)


class SchedulePublicPastManager(ScheduleManager):
    def get_query_set(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        return super(SchedulePublicPastManager, self).get_query_set().filter(end_time__lte=now, course__is_active=1, course_status=3)


class Schedule(Durational):
    """
    """
    class Meta:
        verbose_name        = 'Class Schedule'
        verbose_name_plural = 'Class Schedules'
        ordering            = ['course_status', 'start_time', '-venue']
		
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Contacted'),
        (2, 'Updated'),
        (3, 'Approved'),
        (4, 'Rejected')
    )

    venue           = ForeignKey(Venue, null=True, blank=True, help_text="Where is this class taking place?")
    course          = ForeignKey(Course, help_text="What class are you scheduling?")
    course_status   = SmallIntegerField(max_length=1, choices=STATUS_CHOICES, default=0, help_text="What is the current status of the class?")
    students        = ManyToManyField(Person, through="Registration")    
    items           = ManyToManyField(BarterItem)    
    slug            = SlugField(max_length=120,blank=False, null=True, unique=True, verbose_name="URL Slug")

    objects   = ScheduleManager()
    public    = SchedulePublicManager()
    past      = SchedulePublicPastManager()

    @property
    def is_within_a_day(self):
        now = datetime.utcnow().replace(tzinfo=utc) 
        if (self.start_time - now) < timedelta(hours=24):
            return True
        return False

    @property
    def is_past(self):
        now = datetime.utcnow().replace(tzinfo=utc) 
        if self.end_time < now:
            return True
        return False

    def populate_notifications(self):
        "resets course notification templates from the branch notification templates"
                
        # delete existing branch emails
        schedule_emails = ScheduleEmailContainer.objects.filter(schedule=self).delete()
            
        # copy course notification from the branch notification templates
        branch_email_container = BranchEmailContainer.objects.filter(branch__in=self.course.branch.all())[0]
        
        schedule_email_container = ScheduleEmailContainer(schedule=self)
        
        for fieldname, email_obj in branch_email_container.emails.iteritems():
            new_email = copy_model_instance(email_obj)
            if isinstance(new_email, TimedEmail):
                new_email.set_send_on(self.start_time)
            new_email.save()
            setattr(schedule_email_container, fieldname, new_email)
        schedule_email_container.save()

    def approve_courses(self, request, queryset):
        "approve multiple courses"
        rows_updated = queryset.update(course_status=3)
        if rows_updated == 1:
            message_bit = "1 class was"
        else:
            message_bit = "%s classes were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)        
    approve_courses.short_description = "Approve Classes"

    def save(self, *args, **kwargs):
        """ check if status was changed to approved and email teacher if it has.""" 
        if self.pk is not None:
            original = Schedule.objects.get(pk=self.pk)
            if original.course_status != self.course_status and self.course_status == 3:
                self.emails.email_teacher(self.emails.teacher_class_approval)
        super(Schedule, self).save(*args, **kwargs)

    def __unicode__ (self):
        return "%s" % (self.course.title)


class Registration(Base):
    """
    Registrations represent connections between students and classes.
    When a student registers to a class a registration row is added.
    We do this because we also want to keep track of students who registered
    and then unregistered from a class.
    """
    class Meta:
        unique_together = ('schedule', 'student')
        
    REGISTRATION_CHOICES = (('registered', 'Registered'),('unregistered', 'Unregistereed'))
    
    schedule            = ForeignKey(Schedule)
    student             = ForeignKey(Person, related_name='registrations')
    registration_status = CharField(max_length=20, choices=REGISTRATION_CHOICES, default='registered')
    items               = ManyToManyField(BarterItem, through="RegisteredItem", blank=False)

    def __unicode__ (self):      
        return "%s: %s" % (self.student.fullname, self.registration_status)


class RegisteredItem(Base):
    """

    """

    registration    = ForeignKey(Registration)
    barter_item     = ForeignKey(BarterItem)
    registered      = IntegerField(max_length=3, default=1)
    
    def __unicode__ (self):
        return "%s: %i" % (self.barter_item.title, self.registered)


class Feedback(Base):
    """
    Feedback is collected after courses take place.
    """

    FEEDBACK_TYPE_CHOICES = (('teacher', 'From the Teacher'),('student', 'From a student'))    

    schedule      = ForeignKey(Schedule)
    feedback_type = CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='student')
    content       = TextField(verbose_name='Your Feedback', help_text='your feedback')
        
    def __unicode__ (self):
        return u'%s: feedback %s' % (self.schedule.course.title, self.feedback_type)


class Photo(Base):
    """
    Each branch has photos that can go in a gallery
    """
    class Meta:
        ordering = ['position',]

    def upload_path(self, filename):
        return "uploads/%s/images/%s" % (self.branch.slug, filename)
    
    filename    = ImageField("Photo",upload_to=upload_path)    
    position    = PositiveSmallIntegerField('Position', default=0)    
    branch      = ForeignKey(Branch, help_text="What tradeschool is this object related to?")
        
    def thumbnail(self):
        if self.filename:
            return u'<img src="%s" class="branch_image" />' % self.filename.url
        else:
            return '(No Image)'
        
    def __unicode__ (self):
        return "%s: %s" % (self.branch.title, self.filename)
        

class BranchPage(FlatPage, Base):
    """Extending the FlatPage model to provide branch-specific content pages."""

    branch   = ForeignKey(Branch)
    position = PositiveSmallIntegerField('Position', default=0)    


# signals are separated to signals.py 
# just for the sake of organization
import signals