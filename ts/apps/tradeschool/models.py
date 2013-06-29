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
    
    # Translators:  Used wherever a created time stamp is needed.                   
    created     = DateTimeField(verbose_name=_("created"), editable=False)
    
    # Translators: Used wherever an update time stamp is needed.
    updated     = DateTimeField(verbose_name=_("updated"), editable=False)
    
    # Translators: Used to determine whether something is active in the front end or not.
    is_active   = BooleanField(verbose_name=_("is active"), default=1)
    
    def save(self, *args, **kwargs):
        """ Save timezone-aware values for created and updated fields.
        """
        if self.pk is None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Base, self).save(*args, **kwargs)
        
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
        # Translators: Determines the status of an e-mail - disabled.
        ('disabled', _('Disabled')),
        
        # Translators: Determines the status of an e-mail - Not Sent.
        ('not_sent', _('Not Sent Yet')),
        
        # Translators: Determines the status of an e-mail - Sent.
        ('sent', _('Sent'))
    )
    
    # Translators: The subject of an e-mail.
    subject      = CharField(verbose_name=_("subject"), max_length=140)
    
    # Translators: The content of an e-mail.
    content      = TextField(verbose_name=_("content"))
    
    # Translators: The status of an e-mail. See the Toople list above. 
    email_status = CharField(verbose_name=_("email status"), max_length=30, choices=EMAIL_CHOICES, default='not_sent')

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
    
    # Translators: The date for when an e-mail will be sent.
    send_on      = DateTimeField(verbose_name=_("Send on"), blank=True, null=True)
    
    # Translators: How many days before the class the email will be sent.
    days_delta   = IntegerField(verbose_name=_("Days before"), default=-1)
    
    # Translators: The time for when an e-mail will be sent.
    send_time    = TimeField(verbose_name=_("Send time"), default=time(10,0,0))

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
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Student confirmation")
        
        # Translators: Plural.
        verbose_name_plural = _("Student confirmations")
        
class StudentReminder(TimedEmail):
    """An email that is sent to a registered student a day before a class is scheduled to start."""
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Student reminder")
        
        # Translators: Plural.
        verbose_name_plural = _("Student reminders")
    
    def save(self, *args, **kwargs):
        self.days_delta = -1
        self.send_time = time(10,0,0)
        super(StudentReminder, self).save(*args, **kwargs)


class StudentFeedback(TimedEmail):
    """An email that is sent to a student a day after a scheduled class took place."""

    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Student feedback e-mail")
        
        # Translators: Plural.
        verbose_name_plural = _("Student feedback e-mails")

    def save(self, *args, **kwargs):
        self.days_delta = 1
        self.send_time = time(16,0,0)
        super(StudentFeedback, self).save(*args, **kwargs)


class TeacherConfirmation(Email):
    """An email that is sent when a teacher submitted a class."""

    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Teacher confirmation")
        
        # Translators: Plural.
        verbose_name_plural = _("Teacher confirmations")


class TeacherClassApproval(Email):
    """An email that is sent when an admin approved a teacher submitted a class."""
    pass                                 


class TeacherReminder(TimedEmail):
    """An email that is sent to a teacher a day before their class takes place."""
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Teacher reminder")
        
        # Translators: Plural.
        verbose_name_plural = _("Teacher reminders")
    
    def save(self, *args, **kwargs):
        self.days_delta = -1
        self.send_time = time(18,0,0)
        super(TeacherReminder, self).save(*args, **kwargs)


class TeacherFeedback(TimedEmail):
    """An email that is sent to a teacher a day after a scheduled class took place."""

    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Teacher feedback e-mail")
        
        # Translators: Plural.
        verbose_name_plural = _("Teacher feedback e-mails")
        
    def save(self, *args, **kwargs):
        self.days_delta = 1
        self.send_time = time(18,0,0)
        super(TeacherFeedback, self).save(*args, **kwargs)


class EmailContainer(Base):
    """
    """
    class Meta:
        abstract = True
    
    # Translators: In the Branch E-mail page, the label for student confirmation e-mail
    student_confirmation   = ForeignKey(StudentConfirmation, verbose_name=_("Student Confirmation"))
    
    # Translators: ... The lable for Student Reminder e-mail
    student_reminder       = ForeignKey(StudentReminder, verbose_name=_("Student Reminder"))
    
    # Translators: ... The lable for Student Feedback e-mail
    student_feedback       = ForeignKey(StudentFeedback, verbose_name=_("Student Feedback"))
    
    # Translators: ... The lable for Teacher confirmation e-mail
    teacher_confirmation   = ForeignKey(TeacherConfirmation, verbose_name=_("Teacher Confirmation"))
    
    # Translators: ... The lable for Teacher Class Approval e-mail
    teacher_class_approval = ForeignKey(TeacherClassApproval, verbose_name=_("Teacher Class Approval"))
    
    # Translators: ... The lable for Teacher Reminder e-mail
    teacher_reminder       = ForeignKey(TeacherReminder, verbose_name=_("Teacher Reminder"))
    
    # Translators: ... The lable for Teacher Feedback e-mail
    teacher_feedback       = ForeignKey(TeacherFeedback, verbose_name=_("Teacher Feedback"))

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
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Default e-mail container")
        
        # Translators: Plural.
        verbose_name_plural = _("Default e-mail containers")

class Location(Base):
    """
    Abstract for location based models: branch & venue.     
    """
    class Meta:
        abstract = True
    
    title   = CharField(
                    # Translators: This is for the name of a Trade School location or venue.
                    verbose_name=_("title"), 
                    max_length=100, 
                    # Translators: Contextual Help.
                    help_text=_("The name of the space")
                )
    
    phone   = CharField(
                    verbose_name=_("phone"),
                    max_length=30, 
                    blank=True, 
                    null=True,
                    # Transalators: Contextual Help. 
                    help_text=_("Optional.")
                )
    
    city    = CharField(
                    verbose_name=_("city"),
                    max_length=100
                )
    
    state   = USStateField(
                    verbose_name=_("state"),
                    null=True, 
                    blank=True,
                    # Translators: Contextual Help
                    help_text=_("If in the US.")
                )
    
    country = CountryField(
                    verbose_name=_("country")
                )


class BranchEmailContainerManager(Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(BranchEmailContainerManager, self).get_query_set().select_related()


class BranchEmailContainer(EmailContainer):
    """
    """        
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Branch Emails")
        
        # Translators: Plural.
        verbose_name_plural = _("Branch Emails")
    
    branch = OneToOneField("Branch", verbose_name=_("branch"), related_name="emails")

    objects = BranchEmailContainerManager()
    
    def __unicode__ (self):
        return u"for %s" % self.branch.title


class Cluster(Base):
    """Branches can be grouped together for possibly displaying them together on the website.
        For example: multiple branches in one city can belong to the same group."""
    
    # Translators: The name of a cluster if there is one.    
    name = CharField(verbose_name=_("name"), max_length=100) 


class Branch(Location):
    """
    A branch is a ts organization in a specific location (usually city/region).
    The branch slug should be used to point to the individual branch app functionality.
    All dates and times in the branch's view templates should reflect the branch's timezone.   
    """    
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Branch')
        
        # Translators: Plural.
        verbose_name_plural = _('Branches')
        
        ordering = ['title']
        
    COMMON_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    
    slug        = SlugField(
                        # Translators: This is the part that comes after tradeschool.coop/ en el URL.
                        verbose_name=_("slug"),
                        max_length=120, 
                        # Translators: Contextual Help.
                        help_text=_("This is the part that comes after 'http://tradeschool.coop/' in the URL")
                    )
                     
    email       = EmailField(verbose_name=_("e-mail"), max_length=100)
    timezone    = CharField(verbose_name=_("timezone"), max_length=100, choices=COMMON_TIMEZONE_CHOICES)
    language    = CharField(verbose_name=_("language"), max_length=50, choices=settings.LANGUAGES, null=True)
    organizers  = ManyToManyField(User, verbose_name=_("organizers"))
    
    # Translators: This is the Branches domain address.
    site        = ForeignKey(Site, verbose_name=_("site"), default=Site.objects.get_current())
    
    # Translators: If this Trade School belogns to a set of Trade Schools.
    cluster     = ForeignKey(Cluster, verbose_name=_("cluster"), null=True)
    
    # Translators: This is the part that says 'Barter for Knowledge' which is also editable.
    header_copy = HTMLField(verbose_name=_("header"), null=True, blank=True, default="Barter for knowledge")
    
    # Translators: This is the part with room for a small statement.
    intro_copy  = HTMLField(verbose_name=_("intro"), null=True, blank=True)
    
    # Translators: This is the part at the end of the page. 
    footer_copy = HTMLField(verbose_name=_("footer"), null=True, blank=True)

    objects   = Manager()
    on_site   = CurrentSiteManager()

    
    def save(self, *args, **kwargs):
        """Check to see if the slug field's value has been changed. 
        If it has, rename the branch's template dir name."""
        
        template_directory = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.slug)

        if self.pk is not None and os.path.exists(template_directory):
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
    class Meta:
        ordering = ['branch', 'is_active', 'title']
        
    
    TYPE_CHOICES = ((0, 'Normal'), (1, 'Alternative'))

    def random_color():
        colorValue = random.randint(0, 16777215)
        return "#%x" % colorValue

    venue_type  = SmallIntegerField(max_length=1, choices=TYPE_CHOICES, default=0) 
    address_1   = CharField(max_length=200, verbose_name=_("Address 1"))
    address_2   = CharField(max_length=100, blank=True, null=True, verbose_name=_("Address 2"))
    capacity    = SmallIntegerField(
                        max_length=4, 
                        default=20, 
                        # Translators: the capacity of the venue where you are hosting classes.
                        verbose_name=_("capacity"),
                        # Translators: Contextual Help
                        help_text=_("How many people fit in the space?")
                    )
                    
    resources   = TextField(
                        # Translators: The field name for resources of a venue.
                        verbose_name=_("resources"),
                        null=True, 
                        default="For Example: Chairs, Tables",
                        # Translators: Contextual Help 
                        help_text=_("What resources are available at the space?")
                    )
    color       = CharField(verbose_name=_("color"), max_length=7, default=random_color)
    branch      = ForeignKey(
                        Branch, 
                        verbose_name=_("branch"), 
                        help_text="What tradeschool is this object related to?"
                    )


class PersonManager(Manager):
    use_for_related_fields = True
    
    def get_query_set(self):
        return super(PersonManager, self).get_query_set().annotate(
            registration_count  =Count('registrations', distinct=True), 
            courses_taught_count=Count('courses_taught', distinct=True)
        ).select_related().prefetch_related('branch')


class Person(Base):
    """
    Person in the tradeschool system is either a teacher or a student.
    A person submitting a class as a teacher will have to supply a bio as well.
    """
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = "Person"
        
        # Translators: Plural.
        verbose_name_plural = "People"
        
        ordering = ['fullname', ]
        
    fullname    = CharField(
                        max_length=200, 
                        verbose_name=_("your name"), 
                        # Translators: Contextual Help.
                        help_text=_("This will appear on the site.")
                    )
                    
    email       = EmailField(
                        max_length=100, 
                        verbose_name=_("Email address"),
                        # Translators: Contextual Help. 
                        help_text=_("Used only for us to contact you.")
                    )
                    
    phone       = CharField(
                        max_length=20, 
                        blank=True, 
                        null=True, 
                        verbose_name=_("Phone number"), 
                        # Translators: Contextual Help
                        help_text=_("Optional. Used only for us to contact you.")
                    )
                        
    bio         = TextField(
                        blank=True, 
                        verbose_name=_("A few sentences about you"), 
                        # Translators: Contextual Help
                        help_text=_("For prospective students to see on the website")
                    )
                    
    website     = URLField(
                        max_length=200, 
                        blank=True, 
                        null=True, 
                        verbose_name=_("Your website / blog URL"), 
                        # Translators: Contextual Help
                        help_text=_("Optional.")
                    )
                    
    slug        = SlugField(max_length=220, verbose_name="URL Slug", help_text="This will be used to create a unique URL for each person in TS.")
    branch      = ManyToManyField(
                        Branch, 
                        verbose_name=_("branch"), 
                        # Translators: Contextual Help
                        help_text=_("What tradeschool is this object related to?")
                    )
    
    objects = PersonManager()

    def branches(self):
        """ Return the branches that this registration relates to. This function is used in the admin list_display() method."""
        return ','.join( str(branch) for branch in self.branch.all())
        
    def __unicode__ (self):
        return self.fullname
            

class TeacherManager(PersonManager):
    use_for_related_fields = True    
    def get_query_set(self):
        return super(TeacherManager, self).get_query_set().filter(courses_taught_count__gt=0)


class Teacher(Person):
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Teacher")
        
        # Translators: Plural.
        verbose_name_plural = _("Teachers")
        
        proxy = True
        
    objects = TeacherManager()


class StudentManager(PersonManager):
    use_for_related_fields = True    
    def get_query_set(self):
        return super(StudentManager, self).get_query_set().filter(registration_count__gt=0)


class Student(Person):
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Student")
        
        # Translators: Plural.
        verbose_name_plural = _("Students")
        
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
        
        ordering = ['title',]

    CATEGORIES = (
        (0, 'Arts'),
        (1, 'Etc'),
        (2, 'Food'),
        (3, 'Info'),
        (4, 'Lit'),
        (5, 'Music'),
        (6, 'Org')
    )
    
    teacher         = ForeignKey(Person, verbose_name=_("teacher"), related_name='courses_taught')
    category        = SmallIntegerField(max_length=1, choices=CATEGORIES, default=random.randint(0, 6))    
    max_students    = IntegerField(max_length=4, verbose_name=_("Maximum number of students in your class"))
    title           = CharField(max_length=255, verbose_name=_("class title")) 
    slug            = SlugField(max_length=255,blank=False, null=True, verbose_name=_("URL Slug"))
    description     = TextField(blank=False, verbose_name=_("Class description"))
    branch          = ManyToManyField(Branch, help_text="What tradeschool is this object related to?")

    objects = Manager()
    

class Durational(Base):
    """
    Durational is an abstract model for any model that has a start time and an end time.
    In the tradeschool system, these would be the Time and Course models.
    """
    class Meta:
		abstract = True
		
    # Translators: Used to lable the beginning and endings of classes
    start_time  = DateTimeField(verbose_name=_("start time"), default=datetime.now())
    
    # Translators: Used to lable the beginning and endings of classes
    end_time    = DateTimeField(verbose_name=_("end time"), default=datetime.now())
    
    
class Time(Durational):
    """
    Time is an open time slot. It is implemented in the frontend alone:
    These slots populate the calendar for teachers submitting a class.
    Times do not affect the admin class schedluing logic.
    """
    
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name        = _("Time Slot")
       
       # Translators: Plural
        verbose_name_plural = _("Time Slots")
    
    venue = ForeignKey(
                Venue, 
                verbose_name=_("venue"), 
                null=True, 
                blank=True, 
                # Translators: Contextual Help
                help_text=_("Is this time slot associated with a specific venue?")
            )
            
    branch = ForeignKey(Branch, help_text="What tradeschool is this object related to?")

    def __unicode__ (self):
        return u"%s" % self.start_time


class TimeRange(Base):
    """
    """
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name        = _("Time Slot Range")
        
        # Translators: Plural.
        verbose_name_plural = _("Time Slot Ranges")

    start_date  = DateField(verbose_name=_("Start date"), default=datetime.now())
    end_date    = DateField(verbose_name=_("End date"), default=datetime.now())
    start_time  = TimeField(verbose_name=_("Start time"), default=datetime(2008, 1, 31, 18, 00, 00))
    end_time    = TimeField(verbose_name=_("End time"), default=datetime(2008, 1, 31, 19, 30, 00))
    sunday      = BooleanField(verbose_name=_("Sunday"))
    monday      = BooleanField(verbose_name=_("Monday"))
    tuesday     = BooleanField(verbose_name=_("Tuesday"))
    wednesday   = BooleanField(verbose_name=_("Wednesday"))
    thursday    = BooleanField(verbose_name=_("Thursday"))
    friday      = BooleanField(verbose_name=_("Friday"))
    saturday    = BooleanField(verbose_name=_("Saturday"))
    
    branch      = ForeignKey(Branch, help_text="What tradeschool is this object related to?")
        

class ScheduleEmailContainer(EmailContainer):
    """
    """
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Schedule Email")
        
        # Translators: Plural
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
    
    def branches(self):
        return ','.join( str(branch) for branch in self.schedule.course.branch.all())
        
    def __unicode__ (self):
        return u"for %s" % self.schedule.course.title


class BarterItem(Base):
    """
    Barter items are the items that teachers request for a class they're teaching.
    The items themselves can be requested in various classes.
    """
    class Meta:
        ordering = ['title', ]
    # Translators: Wherever the barter item shows up.
    title    = CharField(verbose_name=_("title"), max_length=255)
    schedule = ForeignKey('Schedule', verbose_name=_('schedule')) 

    def __unicode__ (self):
        return u"%s" % (self.title,)


class ScheduleManager(Manager):
    use_for_related_fields = True    
    def get_query_set(self):
        qs = super(ScheduleManager, self).get_query_set().annotate(
            registered_students=Count('students')
        ).select_related(
            'venue__title',
            'course__title',
            'course__teacher__fullname',
            'course__teacher__email'
        )

        return qs

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
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name        = _('Class Schedule')
        
        # Translators: Plural
        verbose_name_plural = _('Class Schedules')
        
        ordering            = ['course_status', 'start_time', '-venue']
		
    STATUS_CHOICES = (
        # Translators: The thing that shows what the status of the class is
        (0, _('Pending')),
        (1, _('Contacted')),
        (2, _('Updated')),
        (3, _('Approved')),
        (4, _('Rejected'))
    )

    venue           = ForeignKey(
                            Venue, 
                            verbose_name=_("venue"),
                            null=True, 
                            blank=True, 
                            # Translators: Contextual Help
                            help_text=_("Where is this class taking place?")
                        )
                        
    course          = ForeignKey(
                            Course, 
                            verbose_name=_("course"),
                            # Translators: Contextual Help
                            help_text=_("What class are you scheduling?")
                        )
                        
    course_status   = SmallIntegerField(
                            max_length=1, 
                            verbose_name=_("course status"),
                            choices=STATUS_CHOICES, 
                            default=0, 
                            # Translators: Contextual Help
                            help_text=_("What is the current status of the class?")
                        )
                        
    students        = ManyToManyField(
                            Person, 
                            verbose_name=_("students"),
                            through="Registration"
                        )
                                                        
    slug            = SlugField(max_length=255,blank=False, null=True, unique=True, verbose_name=_("URL Slug"))

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
        schedule_emails = ScheduleEmailContainer.objects.filter(schedule=self)
        if schedule_emails.exists():
            schedule_emails.delete()
            
        # copy course notification from the branch notification templates
        branch_email_containers = BranchEmailContainer.objects.filter(branch__in=self.course.branch.all())
        if branch_email_containers.exists():
            branch_email_container = branch_email_containers[0]
        
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


class RegistrationManager(Manager):
    use_for_related_fields = True    
    def get_query_set(self):
        return super(RegistrationManager, self).get_query_set().select_related('schedule', 'student').prefetch_related('items')


class Registration(Base):
    """
    Registrations represent connections between students and classes.
    When a student registers to a class a registration row is added.
    We do this because we also want to keep track of students who registered
    and then unregistered from a class.
    """
    class Meta:
        unique_together = ('schedule', 'student')
        ordering = ['schedule', 'registration_status', 'student']
        
    # Translators: Student registration buttons.     
    REGISTRATION_CHOICES = (('registered', _('Registered')),
                            ('unregistered', _('Unregistereed')))
    
    schedule            = ForeignKey(Schedule, verbose_name=_("schedule"))
    student             = ForeignKey(Person, verbose_name=_("student"), related_name='registrations')
    registration_status = CharField(verbose_name=_("registration status"), max_length=20, choices=REGISTRATION_CHOICES, default='registered')
    items               = ManyToManyField(BarterItem, verbose_name=_("items"), blank=False)

    objects = RegistrationManager()
    
    def branches(self):
        """ Return the branches that this registration relates to. This function is used in the admin list_display() method."""
        return ','.join( str(branch) for branch in self.schedule.course.branch.all())
    
    def registered_items(self):
        """ Return the registered items as a string. Used in the admin."""
        return ','.join( str(item) for item in self.items.all())        
        
    def __unicode__ (self):      
        return "%s: %s" % (self.student, self.registration_status)


class Feedback(Base):
    """
    Feedback is collected after courses take place.
    """
    # Translations: These next three are for the feedback form.
    FEEDBACK_TYPE_CHOICES = (('teacher', _('From the Teacher')),('student', _('From a student')))    

    schedule      = ForeignKey(Schedule, verbose_name=_("schedule"))
    feedback_type = CharField(verbose_name=_("feedback type"), max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='student')
    # Translators: Contextual Help
    content       = TextField(help_text='your feedback', verbose_name=_('Your Feedback'))
        
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
    
    # Translators: These next three are for the photograph files
    filename    = ImageField(_("Photo"), upload_to=upload_path)    
    position    = PositiveSmallIntegerField(_('Position'), default=0)    
    branch      = ForeignKey(Branch, help_text="What tradeschool is this object related to?")
        
    def thumbnail(self):
        if self.filename:
            return u'<img src="%s" class="branch_image" />' % self.filename.url
        else:
            return '(No Image)'
        
    def __unicode__ (self):
        return "%s: %s" % (self.branch.title, self.filename)
        

class BranchPage(FlatPage, Base):
    """Extending the FlatPage model to provide branch-specific content pages.
    """
    class Meta:
        ordering = ['branch', 'title']
        
    # Translators: These one is for the dynamic custom pages.
    branch   = ForeignKey(Branch, verbose_name=_("branch"))
    position = PositiveSmallIntegerField(_('Position'), default=0)    


# signals are separated to signals.py 
# just for the sake of organization
import signals