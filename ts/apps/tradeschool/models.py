from django.conf import settings
from django.db.models import *
from django.contrib.localflavor.us.models import USStateField
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
#from django_mailer import send_mail
from django.template import Context
from django.template import Template
from django_countries import CountryField
from tinymce.models import HTMLField
import pytz, random, time, shutil, errno, os
from datetime import *
from tradeschool.utils import copy_model_instance, unique_slugify
from tradeschool.widgets import *



class Base(Model):
    """
    Abstract base model for all of the models in the tradeschool application.
    Base has datetime fields to keep a record of the times an object is created and updated.
    The Base model also has an is_active boolean field. is_active is implemented in the following way:
    only objects that are active on will appear on the website. Inactive (is_active=False) objects are 
    still accessible through the admin backend, but would not appear on the site.
    """
    
    class Meta:
        abstract = True
    
    # Translators:  Used wherever a created time stamp is needed.                   
    created     = DateTimeField(verbose_name=_("created"), editable=False, help_text=_("The time when this object was created."))
    
    # Translators: Used wherever an update time stamp is needed.
    updated     = DateTimeField(verbose_name=_("updated"), editable=False, help_text=_("The time when this object was edited last."))
    
    # Translators: Used to determine whether something is active in the front end or not.
    is_active   = BooleanField(verbose_name=_("is active"), default=1, help_text=_("This field indicates whether the object is active on the front end of the site. Inactive objects will still be available through the admin backend."))
    
    def save(self, *args, **kwargs):
        """Save timezone-aware values for created and updated fields."""
        if self.pk is None:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Base, self).save(*args, **kwargs)
        
    def __unicode__ (self):
        if hasattr(self, "title") and self.title:
            return self.title
        else:
            return "%s" % (type(self))


class Email(Model):
    """
    Abstract model for all emails in the TS system.
    site-wide emails, TS branch emails, and schedule-specific emails all extend this model.
    The email's body can include variables that will then be populated with relevant data
    from the Schedule and/or Person that the email is refering to. These variables are populated
    using Django's templates. The content field is used as a template that's created dynamically.
    """
    
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
    subject      = CharField(verbose_name=_("subject"), max_length=140, help_text=_("The subject line of the email."))
    
    # Translators: The content of an e-mail.
    content      = TextField(verbose_name=_("content"), help_text=_("The body of the email."))
    
    # Translators: The status of an e-mail. See the Toople list above. 
    email_status = CharField(verbose_name=_("email status"), max_length=30, choices=EMAIL_CHOICES, default='not_sent', help_text=_("Indicates the current status of the email message. A disabled email won't get sent, a not sent email was not sent yet, and a sent email was sent by the system."))

    branch       = OneToOneField('Branch', null=True, blank=True)
    schedule     = OneToOneField('Schedule', null=True, blank=True)

    def preview(self, schedule_obj, registration=None):
        template = Template(self.content)
        context  = self.template_context(schedule_obj, registration)
        body     = template.render(context)
        
        return body

    def send(self, schedule_obj, recipient, registration=None):
        body    = self.preview(schedule_obj, registration)
        branch  = schedule_obj.course.branches.all()[0]
        send_mail(self.subject, body, branch.email, recipient)
        self.email_status = 'sent'
        self.save()

    def template_context(self, schedule_obj, registration=None):
        """ """
        teacher = schedule_obj.course.teacher
        site    = Site.objects.get_current()
        branch  = Branch.objects.get(pk=schedule_obj.course.branches.all()[0].pk)
        venue   = schedule_obj.venue
        domain  = site.domain
        
        student_feedback_url = "%s%s" % (domain, reverse('schedule-feedback', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug, 'feedback_type': 'student'}))
        teacher_feedback_url = "%s%s" % (domain, reverse('schedule-feedback', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug, 'feedback_type': 'teacher'}))
        class_edit_url       = "%s%s" % (domain, reverse('schedule-edit', kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule_obj.slug,}))
        homepage_url         = "%s%s" % (domain, reverse('schedule-list', kwargs={'branch_slug': branch.slug}))

        student_list = ""
        for registration_obj in schedule_obj.registration_set.all():
            if registration_obj.registration_status == 'registered':
                student_list += "\n%s: " % registration_obj.student.fullname
                student_items = []
                for item in registration_obj.items.all():
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
        if registration is not None:
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
    send_on      = DateTimeField(verbose_name=_("Send on"), blank=True, null=True, help_text=_("This is the time in which the email is scheduled to be sent out automatically by the system. Edit this time if you wish to have the email sent at a different time."))
    
    # Translators: How many days before the class the email will be sent.
    days_delta   = IntegerField(verbose_name=_("Days before"), default=-1, help_text=_("This value is used internally to calculate the email's \"send on\" date. The date is calculated by adding or subtracting as many days as this value from the date the class is scheduled to take place."))
    
    # Translators: The time for when an e-mail will be sent.
    send_time    = TimeField(verbose_name=_("Send time"), default=time(10,0,0), help_text=("This value is used internally to calcualate the email's \"send on\" time. This is the hour in which the email will be set to get sent at."))

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


class EmailContainer(Model):
    """
    """
    class Meta:
        abstract = True
    
    # Translators: In the Branch E-mail page, the label for student confirmation e-mail
    studentconfirmation   = OneToOneField(StudentConfirmation, verbose_name=_("Student Confirmation"), help_text=_("This email is sent to a student's email after they registered to a class successfully."))
    
    # Translators: ... The lable for Student Reminder e-mail
    studentreminder       = OneToOneField(StudentReminder, verbose_name=_("Student Reminder"), help_text=_("This email is sent to all students registered to a class before the class is scheduled to take place."))
    
    # Translators: ... The lable for Student Feedback e-mail
    studentfeedback       = OneToOneField(StudentFeedback, verbose_name=_("Student Feedback"), help_text=_("This email is sent to all students who were registered to a class after the class has taken place. It includes a link for students to submit feedback on the class."))
    
    # Translators: ... The lable for Teacher confirmation e-mail
    teacherconfirmation   = OneToOneField(TeacherConfirmation, verbose_name=_("Teacher Confirmation"), help_text=_("This email is sent to a teacher after they proposed a class using the form on the front end."))
    
    # Translators: ... The lable for Teacher Class Approval e-mail
    teacherclassapproval  = OneToOneField(TeacherClassApproval, verbose_name=_("Teacher Class Approval"), help_text=_("This email is sent to a teacher once their class has been approved by an organizer using the admin backend."))
    
    # Translators: ... The lable for Teacher Reminder e-mail
    teacherreminder       = OneToOneField(TeacherReminder, verbose_name=_("Teacher Reminder"), help_text=_("This email is sent to a teacher before the class they're teaching is scheduled to take place."))
    
    # Translators: ... The lable for Teacher Feedback e-mail
    teacherfeedback       = OneToOneField(TeacherFeedback, verbose_name=_("Teacher Feedback"), help_text=_("This email is sent to a teacher who taught a class after it has taken place. It includes a link for the teacher to submit feedback about their experience."))

    def emails():
        def fget(self):
            return {"studentconfirmation"   : self.studentconfirmation, 
                    "studentreminder"       : self.studentreminder, 
                    "studentfeedback"       : self.studentfeedback,
                    "teacherconfirmation"   : self.teacherconfirmation, 
                    "teacherclassapproval"  : self.teacherclassapproval, 
                    "teacherreminder"       : self.teacherreminder, 
                    "teacherfeedback"       : self.teacherfeedback
                    }
        return locals()

    emails = property(**emails())

    def delete_emails(self):
        # delete existing  emails
        for fieldname, email_obj in self.emails.iteritems():
            email_obj.delete()        


class DefaultEmailContainer(Base, EmailContainer):
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
    def get_query_set(self):
        return super(BranchEmailContainerManager, self).get_query_set().select_related()


class Cluster(Base):
    """
    Branches can be grouped together for possibly displaying them together on the website.
    For example: multiple branches in one city can belong to the same group.
    """
    class Meta:
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Branch Cluster')
        
        # Translators: Plural.
        verbose_name_plural = _('Branch Clusters')
        
        ordering = ['name']

    # Translators: The name of a cluster if there is one.    
    name = CharField(verbose_name=_("name"), max_length=100)
    slug = SlugField(   unique=True,
                        # Translators: This is the part that comes after tradeschool.coop/ en el URL.
                        verbose_name=_("slug"),
                        max_length=120, 
                        # Translators: Contextual Help.
                        help_text=_("This is the part that comes after 'http://tradeschool.coop/cluster/' in the URL")
                    )
    def branches_string(self):
        """ Return the branches that this cluster relates to. This function is used in the admin list_display() method."""
        return ','.join( str(branch) for branch in self.branch_set.all())
    branches_string.short_description = _('branches')

    def save(self, *args, **kwargs):
        """ check if there is slug and create one if there isn't.""" 
        if self.slug == None or self.slug.__len__() == 0:
            self.slug = unique_slugify(Cluster, self.name)

        # call the super class's save method   
        super(Cluster, self).save(*args, **kwargs)

    def __unicode__ (self):
        return u"%s" % self.name

class BranchManager(Manager):
    def get_query_set(self):
        return super(BranchManager, self).get_query_set().select_related(
            'studentconfirmation',
            'studentreminder',
            'studentfeedback',
            'teacherconfirmation',
            'teacherclassapproval',
            'teacherreminder',
            'teacherfeedback',   
        )


class BranchPublicManager(BranchManager):
    def get_query_set(self):
        return super(BranchPublicManager, self).get_query_set().exclude(branch_status='pending').filter(is_active=True)


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
    
    STATUS_CHOICES = (
        # Translators: The thing that shows what the status of the class is
        ('pending', _('Pending')),
        ('setting_up', _('Setting up')),
        ('in_session', _('In Session'))
    )        
    
    COMMON_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    
    slug        = SlugField(
                        # Translators: This is the part that comes after tradeschool.coop/ en el URL.
                        verbose_name=_("slug"),
                        max_length=120, 
                        # Translators: Contextual Help.
                        help_text=_("This is the part that comes after 'http://tradeschool.coop/' in the URL")
                    )
                     
    email       = EmailField(verbose_name=_("e-mail"), max_length=100)
    timezone    = CharField(verbose_name=_("timezone"), max_length=100, choices=COMMON_TIMEZONE_CHOICES, help_text=_("The local timezone in the area where this branch of TS is taking place. The timezone is used to calculate all the class and email times."))
    language    = CharField(verbose_name=_("language"), max_length=50, choices=settings.LANGUAGES, null=True, help_text=_("Setting this language will cause both the front end and the backend of the site to try to load text from the translation strings stored in the system. Text that wasn't translated will fallback on the English version of it."))
    organizers  = ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("organizers"), related_name='branches_organized', db_column='person_id', help_text=_("Select multiple users who help organize this branch of TS. People selected in this box will have access to the branch's data on the admin backend."))
    
    branch_status   = CharField(
                            max_length=50, 
                            verbose_name=_("branch status"),
                            choices=STATUS_CHOICES, 
                            default='pending', 
                            # Translators: Contextual Help
                            help_text=_("What is the current status of this branch?")
                        )
    
    # Translators: This is the Branches domain address.
    site        = ForeignKey(Site, verbose_name=_("site"), help_text=_("The TS system can be installed on several different domains, and still be managed using the same admin backend. This field indicates what installation of the software the branch is related to, meaning, what website do you go to in order to access it."))
    
    # Translators: If this Trade School belogns to a set of Trade Schools.
    cluster     = ForeignKey(Cluster, verbose_name=_("cluster"), null=True, blank=True, help_text=_("TS branches can be grouped together in clusters. This is used mostly to be able to present them together on the same page. For example, all branches in East Coast can belong to the East Coast cluster, and accessed via a separate web page."))
    
    # Translators: This is the part that says 'Barter for Knowledge' which is also editable.
    header_copy = HTMLField(verbose_name=_("header"), null=True, blank=True, default="Barter for knowledge", help_text=_("This text appears in the header of the website."))
    
    # Translators: This is the part with room for a small statement.
    intro_copy  = HTMLField(verbose_name=_("intro"), null=True, blank=True, default="Information for the header of the page", help_text=_("This text appears under the header. Usually it gives brief information about the current session and has a link to submit class proposals."))
    
    # Translators: This is the part at the end of the page. 
    footer_copy = HTMLField(verbose_name=_("footer"), null=True, blank=True, default="Information for the footer of the page", help_text=_("This text appears on the footer of the page. It's optional."))

    def emails():
        def fget(self):
            try:
                return {"studentconfirmation"   : self.studentconfirmation, 
                        "studentreminder"       : self.studentreminder, 
                        "studentfeedback"       : self.studentfeedback,
                        "teacherconfirmation"   : self.teacherconfirmation, 
                        "teacherclassapproval"  : self.teacherclassapproval, 
                        "teacherreminder"       : self.teacherreminder, 
                        "teacherfeedback"       : self.teacherfeedback
                        }
            except:
                pass
        return locals()

    emails = property(**emails()) 

    objects   = BranchManager()
    public    = BranchPublicManager()
    on_site   = CurrentSiteManager()

    
    def save(self, *args, **kwargs):
        """Check to see if the slug field's value has been changed. 
        If it has, rename the branch's template dir name."""
        
        self.site = Site.objects.get_current()
        
        template_directory = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.slug)

        if self.pk is not None and os.path.exists(template_directory):
            original = Branch.objects.get(pk=self.pk)
            if original.slug != self.slug:
                self.update_template_dir(original.slug, self.slug)
        super(Branch, self).save(*args, **kwargs)        
    
    def delete_emails(self):
        # delete existing  emails
        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                email_obj
                email_obj.delete()  

    def populate_notifications(self):
        "resets branch notification templates from the global branch notification templates"
        
        # delete existing emails
        self.delete_emails()

        # copy branch notification from the branch notification templates
        default_email_container = DefaultEmailContainer.objects.all()[0]
        
        for fieldname, email_obj in default_email_container.emails.iteritems():
            new_email = copy_model_instance(email_obj)
            new_email.branch = self
            new_email.save()
    
    def copy_teacher_info_page(self):
        "Creates a copy of the teacher info flatpage for each new branch that gets created."
        
        try:
            branch_page = BranchPage.objects.get(pk=7)
        
            branch_page_copy = copy_model_instance(branch_page)
        
            branch_page_copy.branch = self
        
            branch_page_copy.save()
        except BranchPage.DoesNotExist:
            pass

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
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Venue')
    
        # Translators: Plural
        verbose_name_plural = _('Venues')

    def random_color():
        colorValue = random.randint(0, 16777215)
        return "#%x" % colorValue

    address_1   = CharField(max_length=200, verbose_name=_("Address 1"), )
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
    color       = CharField(verbose_name=_("color"), max_length=7, default=random_color, help_text=_("A hex value HTML color in the form of #123456"))
    branch      = ForeignKey(
                        Branch, 
                        verbose_name=_("branch"), 
                        help_text="What branch of TS is this venue related to?"
                    )


class PersonManager(BaseUserManager):    

    def create_user(self, email, fullname=None, username=None, password=None, is_staff=False, **extra_fields):
        """
        Creates and saves a Person with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('An email must be set')
        if fullname:
            username = unique_slugify(Person, fullname, 'username')
        if not password:
            password = self.make_random_password()
            
        email = self.normalize_email(email)
        
        person = self.model(
                email        = email, 
                username     = username, 
                fullname     = fullname,
                is_staff     = is_staff, 
                is_active    = True, 
                is_superuser = False,
                last_login   = now, 
                **extra_fields
            )

        person.set_password(password)
        person.save(using=self._db)
        return person

    def create_superuser(self, email, password, username=None, fullname=None, **extra_fields):
        person = self.create_user(email, fullname, username, password, **extra_fields)
        person.is_staff = True
        person.is_active = True
        person.is_superuser = True
        person.save(using=self._db)
        return person   
            
    def get_query_set(self):
        return super(PersonManager, self).get_query_set().annotate(
            registration_count  =Count('registrations', distinct=True), 
            courses_taught_count=Count('courses_taught', distinct=True)
        ).select_related().prefetch_related('branches')


class Person(AbstractBaseUser, PermissionsMixin, Base):
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
                    
    username    = CharField(
                        max_length=200, 
                        unique=True,                        
                        verbose_name=_("username"),
                        help_text=_("This is used to login to the site.")
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
    branches    = ManyToManyField(
                        Branch, 
                        verbose_name=_("branch"), 
                        # Translators: Contextual Help
                        help_text=_("People in the TS system can be related to many TS branches. This relationship is made when a person either teaches or registers to a class.")
                    )
    language    = CharField(verbose_name=_("backend language"), default='en', max_length=50, choices=settings.LANGUAGES, null=True, help_text=_("Setting this language will cause the admin backend to try to load text from the translation strings stored in the system FOR THIS USER ONLY. Text that wasn't translated will fallback on the English version of it."))
                    
    is_staff    = BooleanField(
                        _('staff status'), 
                        default=False,
                        help_text=_('Designates whether the user can log into this admin site.')
                    )                    
    
    objects = PersonManager()
    
    USERNAME_FIELD = 'username'

    def branches_string(self):
        """ Return the branches that this person relates to. This function is used in the admin list_display() method."""
        return ','.join( str(branch) for branch in self.branches.all())
    branches_string.short_description = _('branches')

    def branches_organized_string(self):
        """ Return the branches that this person organizes. This function is used in the admin list_display() method."""
        return ','.join( str(branch) for branch in self.branches_organized.all())        
    branches_organized_string.short_description = _('branches')
        
    def get_full_name(self):
        return self.fullname
    
    def get_short_name(self):
        return self.fullname    

    def get_absolute_url(self):
        return '/people/%s/' % urlquote(self.slug)

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __unicode__ (self):
        return self.fullname
            

class OrganizerManager(PersonManager):
    def get_query_set(self):
        return super(OrganizerManager, self).get_query_set().filter(is_staff=True)


class Organizer(Person):
    class Meta:

        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Organizer")

        # Translators: Plural.
        verbose_name_plural = _("Organizers")

        proxy = True

    objects = OrganizerManager()


class TeacherManager(PersonManager):
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
    
    teacher         = ForeignKey(Person, verbose_name=_("teacher"), related_name='courses_taught', help_text=_("The person teaching this class."))
    category        = SmallIntegerField(max_length=1, choices=CATEGORIES, default=random.randint(0, 6))
    max_students    = IntegerField(max_length=4, verbose_name=_("Maximum number of students in your class"), help_text=_("The maximum number of students that will be able to register to this class."))
    title           = CharField(max_length=255, verbose_name=_("class title"), help_text=_("The name of the class. This will appear on the website.")) 
    slug            = SlugField(max_length=255,blank=False, null=True, verbose_name=_("URL Slug"), help_text=_("A unique URL for the class."))
    description     = TextField(blank=False, verbose_name=_("Class description"), help_text=_("The class's description. This will apear on the website."))
    branches        = ManyToManyField(Branch, help_text="A class can be related to many TS brances. The relationship is made when a class is being taught as part of a TS branch.")

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
        verbose_name        = _("Calendar Open Time Slot")
       
       # Translators: Plural
        verbose_name_plural = _("Calendar Open Time Slots")
    
    venue = ForeignKey(
                Venue, 
                verbose_name=_("venue"), 
                null=True, 
                blank=True, 
                # Translators: Contextual Help
                help_text=_("Time slots can be related to specifc venues. When a time slot that's related a venue is selected by a potential teacher, the proposed class will be booked in that venue. In the case a venue isn't selected, it's up to the organizers to select a venue for a proposed class.")
            )
            
    branch = ForeignKey(
                Branch, 
                verbose_name=_("branch"),
                # Translators: Contextual Help
                help_text=_("A time slot is related to a specific TS branch since it populates the times to choose from in the branch's class proposal form.")
            )

    def __unicode__ (self):
        return u"%s" % self.start_time


class TimeRange(Base):
    """
    """
    class Meta:
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name        = _("Calendar Open Time Slot Range")
        
        # Translators: Plural.
        verbose_name_plural = _("Calendar Open Time Slot Ranges")

    start_date  = DateField(verbose_name=_("Start date"), default=datetime.now(), help_text=_("Pick the start date for the date range. The system will go over all days between this date and the end date and then create available time slots for each day of the week that you choose."))
    end_date    = DateField(verbose_name=_("End date"), default=datetime.now(), help_text=_("Pick the end date for the date range. The system will go over all days between the start date and this date and then create available time slots for each day of the week that you choose."))
    start_time  = TimeField(verbose_name=_("Start time"), default=datetime(2008, 1, 31, 18, 00, 00), help_text=_("This is the start time of the all of the available time slots that are going to be created."))
    end_time    = TimeField(verbose_name=_("End time"), default=datetime(2008, 1, 31, 19, 30, 00), help_text=_("This is the end time of all of the available time slots that are going to be created."))
    sunday      = BooleanField(verbose_name=_("Sunday"), help_text=_("Check this day if you wish to create available times on Sundays in the above date range."))
    monday      = BooleanField(verbose_name=_("Monday"), help_text=_("Check this day if you wish to create available times on Mondays in the above date range."))
    tuesday     = BooleanField(verbose_name=_("Tuesday"), help_text=_("Check this day if you wish to create available times on Tuesdays in the above date range."))
    wednesday   = BooleanField(verbose_name=_("Wednesday"), help_text=_("Check this day if you wish to create available times on Wednesdays in the above date range."))
    thursday    = BooleanField(verbose_name=_("Thursday"), help_text=_("Check this day if you wish to create available times on Thursdays in the above date range."))
    friday      = BooleanField(verbose_name=_("Friday"), help_text=_("Check this day if you wish to create available times on Fridays in the above date range."))
    saturday    = BooleanField(verbose_name=_("Saturday"), help_text=_("Check this day if you wish to create available times on Saturdays in the above date range."))
    venue       = ForeignKey(
                    Venue, 
                    verbose_name=_("venue"), 
                    null=True, 
                    blank=True, 
                    # Translators: Contextual Help
                    help_text=_("All of the avaialble time slots that will be created can be related to a specifc venue. When a time slot that's related a venue is selected by a potential teacher, the proposed class will be booked in that venue. In the case a venue isn't selected, it's up to the organizers to select a venue for a proposed class.")
                )    
    branch      = ForeignKey(
                    Branch, 
                    verbose_name=_("branch"),
                    # Translators: Contextual Help
                    help_text=_("The available time slots will be created for this TS branch only.")
                )


class BarterItem(Base):
    """
    Barter items are the items that teachers request for a class they're teaching.
    The items themselves can be requested in various classes.
    """
    class Meta:
        ordering = ['title', ]
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Barter item')
        
        # Translators: Plural
        verbose_name_plural = _('Barter items')
        
    # Translators: Wherever the barter item shows up.
    title    = CharField(verbose_name=_("title"), max_length=255, help_text=_("A name or short description of the barter item."))
    schedule = ForeignKey('Schedule', verbose_name=_('schedule'), help_text=_("The scheduled class that this barter item is listed for."))


class ScheduleManager(Manager):
    def get_query_set(self):
        qs = super(ScheduleManager, self).get_query_set().annotate(
            registered_students=Count('students')
        ).select_related(
            'venue__title',
            'course__title',
            'course__description',
            'course__max_students',                        
            'course__teacher__fullname',
            'course__teacher__email',
            'course__teacher__phone',            
            'course__teacher__website',            
            'course__teacher__bio',
            'studentconfirmation',
            'studentreminder',
            'studentfeedback',
            'teacherconfirmation',
            'teacherclassapproval',
            'teacherreminder',
            'teacherfeedback',   
        )

        return qs


class Schedule(Durational):
    """
    """
    class Meta:
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Class Schedule')
        
        # Translators: Plural
        verbose_name_plural = _('Class Schedules')
        
        ordering            = ['schedule_status', 'start_time', '-venue']
		
    STATUS_CHOICES = (
        # Translators: The thing that shows what the status of the class is
        ('pending', _('Pending')),
        ('contacted', _('Contacted')),
        ('updated', _('Updated')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected'))
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
                        
    schedule_status = CharField(
                            max_length=20, 
                            verbose_name=_("course status"),
                            choices=STATUS_CHOICES, 
                            default='pending', 
                            # Translators: Contextual Help
                            help_text=_("What is the current status of the class? Only approved classes appear on the website.")
                        )
                        
    students        = ManyToManyField(
                            Person, 
                            verbose_name=_("students"),
                            through="Registration",
                            help_text=_("The students who registered to this scheduled class, what are they bringing, and whether they cancelled their attendance.")
                        )
                                                        
    slug            = SlugField(max_length=255,blank=True, null=True, unique=True, verbose_name=_("A unique URL for the scheduled class."))

    def emails():
        def fget(self):
            try:
                return {"studentconfirmation"   : self.studentconfirmation, 
                        "studentreminder"       : self.studentreminder, 
                        "studentfeedback"       : self.studentfeedback,
                        "teacherconfirmation"   : self.teacherconfirmation, 
                        "teacherclassapproval"  : self.teacherclassapproval, 
                        "teacherreminder"       : self.teacherreminder, 
                        "teacherfeedback"       : self.teacherfeedback
                        }
            except:
                pass
        return locals()

    emails = property(**emails())

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

    objects   = ScheduleManager()

    def delete_emails(self):
        # delete existing  emails
        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                email_obj
                email_obj.delete()   

    def populate_notifications(self):
        "resets course notification templates from the branch notification templates"
                
        # delete existing branch emails
        self.delete_emails()
            
        # copy course notification from the branch notification templates
        branches = Branch.objects.filter(pk__in=self.course.branches.all())
        if branches.exists():
            branch = branches[0]
        
            for fieldname, email_obj in branch.emails.iteritems():
                new_email = copy_model_instance(email_obj)
                new_email.pk = None
                new_email.branch = None
                if isinstance(new_email, TimedEmail):
                    new_email.set_send_on(self.start_time)
                new_email.schedule = self
                new_email.save()

    def approve_courses(self, request, queryset):
        "approve multiple courses"
        rows_updated = queryset.update(schedule_status='approved')
        if rows_updated == 1:
            message_bit = "1 class was"
        else:
            message_bit = "%s classes were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)        
    approve_courses.short_description = "Approve Classes"

    def send_timed_emails_in_range(self, start_date, end_date):
        """
        """
        email_count = 0

        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                if isinstance(email_obj, TimedEmail):

                    # check if email send on is within range and was not sent yet                  
                    if start_date < email_obj.send_on < end_date and email_obj.email_status == 'not_sent':
                        
                        # email students
                        if isinstance(email_obj, StudentReminder):
                            email_count += self.email_students(self.studentreminder)

                        if isinstance(email_obj, StudentFeedback):
                            email_count += self.email_students(self.studentfeedback)

                        # email teacher
                        if isinstance(email_obj, TeacherReminder):
                            self.email_teacher(self.teacherreminder)
                            email_count += 1

                        if isinstance(email_obj, TeacherFeedback):
                            self.email_teacher(self.teacherfeedback)
                            email_count += 1                            

        # if there is no ScheduleEmailContainer, populate new emails for the Schedule
        else:
            self.populate_notifications()

        return email_count

    def generate_barteritems_from_past_schedule(self):
        """
        Find a past Schedule of the same Course and copy its BarterItem objects.
        """
        
        # find a scheduled course to this Schedule's course, which is not this one
        past_schedules = Schedule.objects.filter(course=self.course).exclude(pk=self.pk)

        if past_schedules.exists():

            # create copies of the past schedule's BarterItem objects.
            # reset the pk for each one so a new object is saved,
            # and create a relationship to the current Schedule.
            for item in past_schedules[0].barteritem_set.all():
                new_item = copy_model_instance(item)
                new_item.pk = None 
                new_item.schedule = self
                new_item.save()        

    def email_teacher(self, email):
        """shortcut method to send an email via the Schedule object."""
        return email.send(self, (self.course.teacher.email,))

    def email_student(self, email, registration):
        """shortcut method to send an email via the Schedule object."""
        return email.send(self, (registration.student.email,), registration)

    def email_students(self, email):
        """shortcut method to send an email via the Schedule object."""
        email_count = 0
        for registration in self.registration_set.all():
            if registration.registration_status == 'registered':
                self.email_student(email, registration)
                email_count += 1
        return email_count

    def save(self, *args, **kwargs):
        """ check if status was changed to approved and email teacher if it has.""" 
        if self.pk is not None:
            original = Schedule.objects.get(pk=self.pk)
            if original.schedule_status != self.schedule_status and self.schedule_status == 'approved':
                self.email_teacher(self.teacherclassapproval)

        # generate and save slug if there isn't one
        if self.slug == None or self.slug.__len__() == 0:
            self.slug = unique_slugify(Schedule, self.course.title)

        # if there are no barter items, try to find another Schedule of the same Course,
        # and copy the BarterItem objects from that one
        if self.barteritem_set.count() == 0:
            pass
            #self.generate_barteritems_from_past_schedule()

        # call the super class's save method   
        super(Schedule, self).save(*args, **kwargs)

    def __unicode__ (self):
        return "%s" % (self.course.title)


class PendingScheduleManager(ScheduleManager):
    def get_query_set(self):
        return super(PendingScheduleManager, self).get_query_set().filter(end_time__gte=timezone.now()).exclude(schedule_status='approved').exclude(schedule_status='rejected')


class PendingSchedule(Schedule):
    class Meta:

        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Pending Scheduled Classes")

        # Translators: Plural.
        verbose_name_plural = _("Pending Scheduled Classes")

        proxy = True

    objects = PendingScheduleManager()



class ApprovedScheduleManager(ScheduleManager):
    def get_query_set(self):
        return super(ApprovedScheduleManager, self).get_query_set().filter(schedule_status='approved', end_time__gte=timezone.now())


class ApprovedSchedulePublicManager(ApprovedScheduleManager):
    def get_query_set(self):
        return super(ApprovedSchedulePublicManager, self).get_query_set().filter(is_active=True)


class ApprovedSchedule(Schedule):
    class Meta:

        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Approved Scheduled Classes")

        # Translators: Plural.
        verbose_name_plural = _("Approved Scheduled Classes")

        proxy = True

    objects = ApprovedScheduleManager()
    public  = ApprovedSchedulePublicManager()


class PastScheduleManager(ScheduleManager):
    def get_query_set(self):
        return super(PastScheduleManager, self).get_query_set().filter(end_time__lte=timezone.now())


class PastSchedulePublicManager(PastScheduleManager):
    def get_query_set(self):
        return super(PastSchedulePublicManager, self).get_query_set().filter(is_active=True, schedule_status='approved')


class PastSchedule(Schedule):
    class Meta:

        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _("Past Scheduled Classes")

        # Translators: Plural.
        verbose_name_plural = _("Past Scheduled Classes")

        proxy = True

    objects = PastScheduleManager()    
    public  = PastSchedulePublicManager()



class RegistrationManager(Manager):
    def get_query_set(self):
        return super(RegistrationManager, self).get_query_set().select_related('schedule', 'student', 'student__fullname', 'items__title').prefetch_related('items')


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
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Registration')
    
        # Translators: Plural
        verbose_name_plural = _('Registrations')
        
    # Translators: Student registration buttons.     
    REGISTRATION_CHOICES = (('registered', _('Registered')),
                            ('unregistered', _('Unregistereed')))
    
    schedule            = ForeignKey(Schedule, verbose_name=_("schedule"), help_text=_("What scheduled class does this registration refer to?"))
    student             = ForeignKey(Person, verbose_name=_("student"), related_name='registrations', help_text=_("Who registered?"))
    registration_status = CharField(verbose_name=_("registration status"), max_length=20, choices=REGISTRATION_CHOICES, default='registered', help_text=_("Did the student cancel?"))
    items               = ManyToManyField(BarterItem, verbose_name=_("items"), blank=False, help_text=_("The barter items that the student said they were bringing to the class."))

    objects = RegistrationManager()
    
    def branches_string(self):
        """ Return the branches that this registration relates to. This function is used in the admin list_display() method."""
        return ','.join( str(branch) for branch in self.schedule.course.branches.all())
    
    def registered_items(self):
        """ Return the registered items as a string. Used in the admin."""
        return ','.join( str(item) for item in self.items.all())        
        
    def __unicode__ (self):      
        return "%s: %s" % (self.student, self.registration_status)


class Feedback(Base):
    """
    Feedback is collected after courses take place.
    """
    class Meta:
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Feedback')
        
        # Translators: Plural
        verbose_name_plural = _('Feedbacks')
        
    # Translations: These next three are for the feedback form.
    FEEDBACK_TYPE_CHOICES = (('teacher', _('From the Teacher')),('student', _('From a student')))    

    schedule      = ForeignKey(Schedule, verbose_name=_("schedule"), help_text=_("Feedback is given for a class that was scheduled and took place."))
    feedback_type = CharField(verbose_name=_("feedback type"), max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='student', help_text=_("Was this feedback given by a student in the class or by the teacher?"))
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
        
        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Photo')
    
        # Translators: Plural
        verbose_name_plural = _('Photos')
    
    def upload_path(self, filename):
        return "uploads/%s/images/%s" % (self.branch.slug, filename)
    
    # Translators: These next three are for the photograph files
    filename    = ImageField(_("Photo"), upload_to=upload_path)
    position    = PositiveSmallIntegerField(_('Position'), default=0, help_text=_("This indicates the order in which the pictures appear on the website."))
    branch = ForeignKey(
                Branch, 
                verbose_name=_("branch"),
                # Translators: Contextual Help
                help_text=_("What TS branch's page is this photo on?")
            )
        
    def thumbnail(self):
        if self.filename:
            return u'<img src="%s" class="branch_image" />' % self.filename.url
        else:
            # Translators: If there are no images
            return _('(No Image)')
        thumbnail.short_description = _('Thumbnail')
        
    def __unicode__ (self):
        return "%s: %s" % (self.branch.title, self.filename)
        

class BranchPage(FlatPage, Base):
    """Extending the FlatPage model to provide branch-specific content pages.
    """
    class Meta:
        ordering = ['branch', 'title']

        # Translators: This is used in the header navigation to let you know where you are.
        verbose_name = _('Branch Page')
    
        # Translators: Plural
        verbose_name_plural = _('Branch Pages')
    
    # Translators: Used to determine whether a page is to be shown on the front page menu or not. set to yes.
    is_visible   = BooleanField(verbose_name=_("is visible"), default=1, help_text=_("This indicates whether a page is listed in the menu or not. Visible pages appear on the menu. Other pages do not, but are still accessible via their URL."))
        
    # Translators: These one is for the dynamic custom pages.
    branch   = ForeignKey(Branch, verbose_name=_("branch"), null=True, blank=True)
    position = PositiveSmallIntegerField(_('Position'), default=0, help_text=_("This indicates the order in which the pages are listed in the menu."))    


# signals are separated to signals.py 
# just for the sake of organization
import signals