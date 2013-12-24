import os
import errno
import shutil
import time
import random
import pytz
from django.conf import settings
from django.db.models import *
from django.db.models.query import QuerySet
from django.contrib.localflavor.us.models import USStateField
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin, BaseUserManager
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
from datetime import *
from tradeschool.utils import copy_model_instance, unique_slugify
from tradeschool.widgets import *


class Base(Model):
    """
    Abstract base model for all of the models in the tradeschool application.

    Attribues:
        created: A datetime indicating the time the object was created.
            Saved as timezone-aware value.
        updtated: A datetime indicating the latest time the object was saved.
            Saved as timezone-aware value.
        is_active: A boolean indicating whether the object should appear
            on the front end of the website. Impleneted through Managers'
            public() queryset method
    """
    class Meta:
        abstract = True

    created = DateTimeField(
        # Translators:  Used wherever a created time stamp is needed.
        verbose_name=_("created"),
        editable=False,
        help_text=_("The time when this object was created.")
    )
    updated = DateTimeField(
        # Translators: Used wherever an update time stamp is needed.
        verbose_name=_("updated"),
        editable=False,
        help_text=_("The time when this object was edited last.")
    )
    is_active = BooleanField(
        # Translators: Used to determine whether something
        # is active in the front end or not.
        verbose_name=_("is active"),
        default=1,
        help_text=_(
            "This field indicates whether the object is active"
            "on the front end of the site. Inactive objects will"
            "still be available through the admin backend."
        )
    )

    def save(self, *args, **kwargs):
        """
        Saves timezone-aware values for created and updated fields.
        """
        # self.pk is None when the object is saved for the first time
        if self.pk is None:
            self.created = timezone.now()

        self.updated = timezone.now()

        super(Base, self).save(*args, **kwargs)

    def __unicode__(self):
        """
        Returning a title attribute if it exists,
        Otherwise returns the object's type.
        """
        if hasattr(self, "title") and self.title:
            return self.title
        else:
            return u"%s" % (type(self))


class Email(Model):
    """
    Abstract model for all emails in the TS system.

    site-wide emails, TS branch emails, and course-specific emails
    all extend this model.

    The email's body can include variables that will then be populated
    with relevant data from the Course and/or Person that the email
    is refering to.
    These variables are populated using Django's template system.
    The content field is used as a template that's created dynamically.

    Attributes:
        subject: A string representing the subject line of the email.
        content: A block of text representing the body of the email.
            Can include variables formatted in the django template language.
            For example:
            {{ course.title }}: taught by {{ course.teacher.fullname }}
        email_status: A string indicating whether the email should be sent
            or not, and whether it was sent already.
        branch: A one-to-one relationship to a Branch. Used if the email is
            used as a template for all of one branch's emails.
        course: A one-to-one relationship to a Course. Used if the email
            is used for a Course.
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

    subject = CharField(
        # Translators: The subject of an e-mail.
        verbose_name=_("subject"),
        max_length=140,
        help_text=_("The subject line of the email.")
    )
    content = TextField(
        # Translators: The content of an e-mail.
        verbose_name=_("content"),
        help_text=_("The body of the email.")
    )
    email_status = CharField(
        # Translators: The status of an e-mail. See the touple above.
        verbose_name=_("email status"),
        max_length=30,
        choices=EMAIL_CHOICES,
        default='not_sent',
        help_text=_(
            "Indicates the current status of the email message."
            "A disabled email won't get sent,"
            "a not sent email was not sent yet,"
            "and a sent email was sent by the system."
        )
    )
    branch = OneToOneField(
        'Branch',
        null=True,
        blank=True
    )
    course = OneToOneField(
        'Course',
        null=True,
        blank=True
    )

    def template_context(self, course_obj, registration=None):
        """
        Prepares variables and generates a Context object for an Email.

        Emails are composed and edited on the admin backend. Since most of
        the people who write them do not know the structure of the data models,
        the variables are simplified and expressed explicitly.

        For example:
        Instead of {{ course.teacher }}, a {{ teacher }} variable
        will also be available

        In addition, variables are created for the various URLs that could be
        included in a typical Trade School email, such as leaving feedback,
        unregistering, editing a class, etc.

        Args:
            course_obj: A Course object that is used to fill in
                the variables in the email's body.
            registration: A Registration object that is used to
                fill in the variables in the email body in case it is
                sent to a registered student.

        Returns:
            A template Context object.
        """
        # simplify variables
        teacher = course_obj.teacher
        branch = course_obj.branch
        venue = course_obj.venue

        # create a string with the registered students for a scheduled class
        student_list = course_obj.student_list_string()

        # create a Context with all of the above variables
        c = Context({
            'course': course_obj,
            'branch': branch,
            'teacher': teacher,
            'venue': venue,
            'student_feedback_url': course_obj.student_feedback_url,
            'teacher_feedback_url': course_obj.teacher_feedback_url,
            'class_edit_url': course_obj.course_edit_url,
            'homepage_url': branch.branch_url,
            'student_list': student_list
        })

        # Emails sent to students require additional variables from
        # the Registration object. If one is passed, create those variables.s
        if registration is not None:

            # create a string with the items the student registered to bring.
            item_list = registration.registered_item_string()

            # add the Registration-related variables to the context
            c.dicts.append({
                'student': registration.student,
                'registration': registration,
                'unregister_url': registration.unregister_url,
                'item_list': item_list
            })

        return c

    def preview(self, course_obj, registration=None):
        """
        Previews an email content.

        Populates a generic Template object with the email's content,
        Then renders it using the Course and/or Registration objects
        that are passed to the function.

        Args:
            course_obj: A Course instance is used to fill in
                the email's data.
            registration: A Registration instance is used to fill in
                data for emails written to students.

        Returns:
            A string with the rendered Template content's
        """
        # instantiate a temlate with the email's content
        template = Template(self.content)

        # create a context using data from the course
        # and/or registration objects
        context = self.template_context(course_obj, registration)

        # render the template with the created context
        body = template.render(context)

        return body

    def send(self, course_obj, recipient, registration=None):
        """
        Sends a rendered email and updates its status.

        Args:
            course_obj: A Course object that is used to fill in
                the variables in the email's body.
            recipient: an email address to send the email to.
            registration: A Registration object that is used to
                fill in the variables in the email body in case it is
                sent to a registered student.
        """
        # render the email's content using the the data from the course
        # and/or registration objects
        body = self.preview(course_obj, registration)

        # the branch's email is used as the "from" address field
        branch = course_obj.branch

        # send the email
        send_mail(self.subject, body, branch.email, recipient)

        # update the email's status to sent
        self.email_status = 'sent'
        self.save()

    def __unicode__(self):
        """
        Returns:
            string of the email's subject
        """
        return u"%s" % self.subject


class TimedEmail(Email):
    """
    Abstract model for all emails that are sent on a specific time.

    Attributes:
        send_on: datetime indicating the time that the email
            is scheduled to be sent on. Can be null if the object represents
            a template for other emails.
        days_delta: an integar that is used to calculate the email's send_on
            property. This is the number of days that will be subtracted from
            the course's start_time attribute.
        send_time: A time indicating the time of day in which
            the email should be sent.
    """
    class Meta:
        abstract = True

    # Translators: The date for when an e-mail will be sent.
    send_on = DateTimeField(
        verbose_name=_("Send on"),
        blank=True,
        null=True,
        help_text=_(
            "This is the time in which the email is scheduled to be sent out "
            "automatically by the system. Edit this time if you wish to have "
            "the email sent at a different time."
        )
    )
    # Translators: How many days before the class the email will be sent.
    days_delta = IntegerField(
        verbose_name=_("Days before"),
        default=-1,
        help_text=_(
            "This value is used internally to calculate the email's "
            "\"send on\"date. The date is calculated by adding or "
            "subtracting as many days as this value from the date "
            "the class is scheduled to take place."
        )
    )
    # Translators: The time for when an e-mail will be sent.
    send_time = TimeField(
        verbose_name=_("Send time"),
        default=time(10, 0, 0),
        help_text=(
            "This value is used internally to calcualate the email's "
            "\"send on\" time. This is the hour in which the email "
            "will be set to get sent at."
        )
    )

    def set_send_on(self, event_datetime):
        """
        Sets the value of the send_on attribute using days_delta and send_time.

        Args:
            event_datetime: a datetime object that will be used
                for the calculation. Most likely a Course.start_time
        """
        # construct a datetime object after adding / subtracting the days delta
        send_datetime = event_datetime + timedelta(days=self.days_delta)

        # create a naive date from send_datetime
        send_date = date(
            send_datetime.year,
            send_datetime.month,
            send_datetime.day
        )

        # combine the date to send the email with the
        # time set in the email object
        send_on_datetime = datetime.combine(send_date, self.send_time)

        # now do timezone conversion
        current_tz = timezone.get_current_timezone()
        localized_datetime = current_tz.localize(send_on_datetime)
        normalized_datetime = utc.normalize(localized_datetime.astimezone(utc))

        # set send_on to normalized datetime
        self.send_on = normalized_datetime


class StudentConfirmation(Email):
    """
    An email that is sent when a student registeres to a scheduled class.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Student confirmation")

        # Translators: Plural.
        verbose_name_plural = _("Student confirmations")


class StudentReminder(TimedEmail):
    """
    A reminder email that is sent to a registered student before
    a class is scheduled to start.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Student reminder")

        # Translators: Plural.
        verbose_name_plural = _("Student reminders")

    def save(self, *args, **kwargs):
        """
        Sets values to days_delta and send_time attributes.
        """
        # student reminders should be sent a day before at 10am.
        # TODO: make this editable per branch / per email.
        self.days_delta = -1
        self.send_time = time(10, 0, 0)

        super(StudentReminder, self).save(*args, **kwargs)


class StudentFeedback(TimedEmail):
    """
    An email that is sent to a student afer a scheduled class took place.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Student feedback e-mail")

        # Translators: Plural.
        verbose_name_plural = _("Student feedback e-mails")

    def save(self, *args, **kwargs):
        """
        Sets values to days_delta and send_time attributes.
        """
        # student reminders should be sent a day after at 4pm.
        # TODO: make this editable per branch / per email.
        self.days_delta = 1
        self.send_time = time(16, 0, 0)
        super(StudentFeedback, self).save(*args, **kwargs)


class TeacherConfirmation(Email):
    """
    An email that is sent when a teacher submits a class course.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Teacher confirmation")

        # Translators: Plural.
        verbose_name_plural = _("Teacher confirmations")


class TeacherClassApproval(Email):
    """
    An email that is sent when an admin approves a teacher submitted course.
    """
    pass


class TeacherReminder(TimedEmail):
    """
    A reminder email that is sent to a teacher before their class takes place.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Teacher reminder")

        # Translators: Plural.
        verbose_name_plural = _("Teacher reminders")

    def save(self, *args, **kwargs):
        """
        Sets values to days_delta and send_time attributes.
        """
        # teachers reminders should be sent a day before at 6pm.
        # TODO: make this editable per branch / per email.
        self.days_delta = -1
        self.send_time = time(18, 0, 0)
        super(TeacherReminder, self).save(*args, **kwargs)


class TeacherFeedback(TimedEmail):
    """
    An email that is sent to a teacher after a scheduled class took place.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Teacher feedback e-mail")

        # Translators: Plural.
        verbose_name_plural = _("Teacher feedback e-mails")

    def save(self, *args, **kwargs):
        """
        Sets values to days_delta and send_time attributes.
        """
        # student reminders should be sent a day after at 6pm.
        # TODO: make this editable per branch / per email.
        self.days_delta = 1
        self.send_time = time(18, 0, 0)
        super(TeacherFeedback, self).save(*args, **kwargs)


class EmailContainer(Model):
    """
    An abstract class that groups the different types of TS emails together.

    Attributes:
        studentconfirmation: A one-to-one relationship with
            a StudentConfirmation email.
        studentreminder: A one-to-one relationship with
            a StudentReminder email.
        studentfeedback: A one-to-one relationship with
            a StudentFeedback email.
        teacherconfirmation: A one-to-one relationship with
            a TeacherConfirmation email.
        teacherclassapproval: A one-to-one relationship with
            a TeacherClassApproval email.
        teacherreminder: A one-to-one relationship with
            a TeacherReminder email.
        teacherfeedback: A one-to-one relationship with
            a TeacherFeedback email.
        emails: Dictionary with all of the email attributes' names and values.
            Used to iterate over the emails easily.
    """
    class Meta:
        abstract = True

    # Translators: In Branch email page, the label for student confirmation
    studentconfirmation = OneToOneField(
        StudentConfirmation,
        verbose_name=_("Student Confirmation"),
        help_text=_(
            "This email is sent to a student's email after they registered "
            "to a class successfully."
        )
    )
    # Translators: ... The label for Student Reminder e-mail
    studentreminder = OneToOneField(
        StudentReminder,
        verbose_name=_("Student Reminder"),
        help_text=_(
            "This email is sent to all students registered to a class before "
            "the class is scheduled to take place."
        )
    )
    # Translators: ... The label for Student Feedback e-mail
    studentfeedback = OneToOneField(
        StudentFeedback,
        verbose_name=_("Student Feedback"),
        help_text=_(
            "This email is sent to all students who were registered to "
            "a class after the class has taken place. It includes a link "
            "for students to submit feedback on the class."
        )
    )
    # Translators: ... The label for Teacher confirmation e-mail
    teacherconfirmation = OneToOneField(
        TeacherConfirmation,
        verbose_name=_("Teacher Confirmation"),
        help_text=_(
            "This email is sent to a teacher after they proposed a class "
            "using the form on the front end."
        )
    )
    # Translators: ... The label for Teacher Class Approval e-mail
    teacherclassapproval = OneToOneField(
        TeacherClassApproval,
        verbose_name=_("Teacher Class Approval"),
        help_text=_(
            "This email is sent to a teacher once their class has been "
            "approved by an organizer using the admin backend."
        )
    )
    # Translators: ... The label for Teacher Reminder e-mail
    teacherreminder = OneToOneField(
        TeacherReminder,
        verbose_name=_("Teacher Reminder"),
        help_text=_(
            "This email is sent to a teacher before the class they're teaching"
            " is scheduled to take place."
        )
    )
    # Translators: ... The label for Teacher Feedback e-mail
    teacherfeedback = OneToOneField(
        TeacherFeedback,
        verbose_name=_("Teacher Feedback"),
        help_text=_(
            "This email is sent to a teacher who taught a class after it has "
            "taken place. It includes a link for the teacher to submit "
            "feedback about their experience."
        )
    )

    def emails():
        def fget(self):
            return {"studentconfirmation": self.studentconfirmation,
                    "studentreminder": self.studentreminder,
                    "studentfeedback": self.studentfeedback,
                    "teacherconfirmation": self.teacherconfirmation,
                    "teacherclassapproval": self.teacherclassapproval,
                    "teacherreminder": self.teacherreminder,
                    "teacherfeedback": self.teacherfeedback
                    }
        return locals()

    emails = property(**emails())

    def delete_emails(self):
        """
        Deletes related email objects
        """
        for fieldname, email_obj in self.emails.iteritems():
            email_obj.delete()


class DefaultEmailContainer(Base, EmailContainer):
    """
    A container for top level Email templates.

    There should be only one instance of this model per TS insatllation.
    The emails in this container are copied each time a Branch is created.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Default e-mail container")

        # Translators: Plural.
        verbose_name_plural = _("Default e-mail containers")


class Location(Base):
    """
    Abstract for location based models: branch & venue.

    Attributes:
        title: A string indicating the name of the location.
        phone: A string indicating the phone number.
        city: A string indicating the city of the location.
        state: A string indicating the state. Currently only has US states
            as options.
        country: A string indicating the country. Uses CountryField
            for choices and validation.
    """
    class Meta:
        abstract = True

    title = CharField(
        # Translators: This is for the name of a Trade School location or venue
        verbose_name=_("title"),
        max_length=100,
        # Translators: Contextual Help.
        help_text=_("The name of the space")
    )
    phone = CharField(
        verbose_name=_("phone"),
        max_length=30,
        blank=True,
        null=True,
        # Transalators: Contextual Help.
        help_text=_("Optional.")
    )
    city = CharField(
        verbose_name=_("city"),
        max_length=100
    )
    state = USStateField(
        verbose_name=_("state"),
        null=True,
        blank=True,
        # Translators: Contextual Help
        help_text=_("If in the US.")
    )
    country = CountryField(
        verbose_name=_("country")
    )


class Cluster(Base):
    """
    Branches can be grouped together in Clusters.

    Clusters can be used to display branches together on the website.
    For example: multiple branches in one city can belong to the same Cluster.

    Attribues:
        name: A string indicating the name of the Cluster.
        slug: A string used to generate URL for a Cluster view.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _('Branch Cluster')

        # Translators: Plural.
        verbose_name_plural = _('Branch Clusters')

        ordering = ['name']

    # Translators: The name of a cluster if there is one.
    name = CharField(
        verbose_name=_("name"),
        max_length=100
    )
    slug = SlugField(
        unique=True,
        # Translators: This is the part that comes after tradeschool.coop/
        verbose_name=_("slug"),
        max_length=120,
        # Translators: Contextual Help.
        help_text=_(
            "This is the part that comes after "
            "'http://tradeschool.coop/cluster/' in the URL"
        )
    )

    def branches_string(self):
        """
        Join related Branch objects in a string.

        This function is used in the admin list_display() method.

        Returns: A string of the branches that this cluster relates to.
        """
        return ','.join(str(branch) for branch in self.branch_set.all())
    branches_string.short_description = _('branches')

    def save(self, *args, **kwargs):
        """
        Check if there is slug and create one if there isn't.
        """
        if self.slug is None or self.slug.__len__() == 0:
            self.slug = unique_slugify(Cluster, self.name)

        # call the super class's save method
        super(Cluster, self).save(*args, **kwargs)

    def __unicode__(self):
        """
        Returns: a unicode string of the Cluster's name attribute.
        """
        return u"%s" % self.name


class BranchQuerySet(QuerySet):
    """
    Defines querysets for public and pending branches.
    """
    def public(self):
        """
        Returns active branches that have either
        'in_session' or 'setting_up' status
        """
        return self.exclude(branch_status='pending').filter(is_active=True)

    def pending(self):
        """
        Returns pending branches
        """
        return self.filter(status='pending')


class BranchManager(Manager):
    """
    A Manager selecting related emails.
    """
    def get_query_set(self):
        """
        Selects related Email objects from the custom QuerySet
        """
        return BranchQuerySet(self.model, using=self._db).select_related(
            'studentconfirmation',
            'studentreminder',
            'studentfeedback',
            'teacherconfirmation',
            'teacherclassapproval',
            'teacherreminder',
            'teacherfeedback',
        )

    def pending(self):
        return self.get_query_set().pending()

    def public(self):
        return self.get_query_set().public()


class Branch(Location):
    """
    A Branch is a chapter of TS in a specific location (usually city/region).

    All querysets except for those used on the Trade School HQ page
    are filtered by branch, both in the front end and back end.

    Attributes:
        slug: A string that's used to construct a URL for the Branch web pages.
            The Branch's slug is used to identify and get the Branch object
            in the different views across the system.
        email: A string that's used to populate the "from" field in emails
            that are sent by the Branch.
        timezone: A pytz timezone value that's used to calculate the times of
            courses, open time slots, created, and updated.
        language: A language code that's used when translating the branch's
            web pages. Read by the django translation framework.
        organizers: M2M relationship with Person objects who are also
            organizing this Branch. Organizers have access to the admin backend
        branch_status: A string indicating the current status of the Branch.
            A 'pending' branch filled out a form to start a trade school,
            A 'setting_up' branch was approved by an organizer
            and is getting ready to open,
            An 'in_session' branch is running.
        site: A django.sites Site that the Branch is related to. Different
            branches could be installed on different servers, but still
            be connected to the same database.
        clusters: M2M relationship with Cluter objects. Indicates what groups
            a Branch is a part of.
        header_copy: Text that's used to populate the Branch's homepage H1 tag.
        intro_copy: Text that's used to populate the copy in the top box on
            the Branch's homepage.
        footer_copy: Text that's used to populate the footer on Branch pages
            that have one.
        emails: A dictonary with the Branch's related Email objects.
        domain: The current Site's domain.
        branch_url: A full URL of the Branch's homepage.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
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

    # create a tuple of timezones from pytz.
    COMMON_TIMEZONE_CHOICES = tuple(
        zip(pytz.all_timezones, pytz.all_timezones)
    )

    slug = SlugField(
        # Translators: This is the part that comes after tradeschool.coop/
        # in the URL.
        verbose_name=_("slug"),
        max_length=120,
        # Translators: Contextual Help.
        help_text=_(
            "This is the part that comes after 'http://tradeschool.coop/'"
            "in the URL"
        )
    )
    email = EmailField(
        verbose_name=_("e-mail"),
        max_length=100
    )
    timezone = CharField(
        verbose_name=_("timezone"),
        max_length=100,
        choices=COMMON_TIMEZONE_CHOICES,
        help_text=_(
            "The local timezone in the area where this branch of TS"
            "is taking place. The timezone is used to calculate all "
            "the class and email times."
        )
    )
    language = CharField(
        verbose_name=_("language"),
        max_length=50,
        choices=settings.LANGUAGES,
        null=True,
        help_text=_(
            "Setting this language will cause both the front end and "
            "the backend of the site to try to load text from the translation "
            "strings stored in the system. Text that wasn't translated will "
            "fallback on the English version of it."
        )
    )
    organizers = ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("organizers"),
        related_name='branches_organized',
        db_column='person_id',
        help_text=_(
            "Select multiple users who help organize this branch of TS. "
            "People selected in this box will have access to the branch's "
            "data on the admin backend."
        )
    )
    branch_status = CharField(
        max_length=50,
        verbose_name=_("branch status"),
        choices=STATUS_CHOICES,
        default='pending',
        # Translators: Contextual Help
        help_text=_("What is the current status of this branch?")
    )
    site = ForeignKey(
        Site,
        # Translators: This is the Branches domain address.
        verbose_name=_("site"),
        help_text=_(
            "The TS system can be installed on several different domains, "
            "and still be managed using the same admin backend. This field "
            "indicates what installation of the software the branch is "
            "related to, meaning, what website do you go to in order to "
            "access it."
        )
    )
    clusters = ManyToManyField(
        Cluster,
        # Translators: If this Trade School belogns to a set of Trade Schools.
        verbose_name=_("clusters"),
        null=True,
        blank=True,
        help_text=_(
            "TS branches can be grouped together in clusters. This is used "
            "mostly to be able to present them together on the same page. "
            "For example, all branches in East Coast can belong to the "
            "East Coast cluster, and accessed via a separate web page."
        )
    )
    header_copy = HTMLField(
        # Translators: This is the part that says 'Barter for Knowledge'
        # which is also editable.
        verbose_name=_("header"),
        null=True,
        blank=True,
        default="Barter for knowledge",
        help_text=_("This text appears in the header of the website."))
    intro_copy = HTMLField(
        # Translators: This is the part with room for a small statement.
        verbose_name=_("intro"),
        null=True,
        blank=True,
        default="Information for the header of the page",
        help_text=_(
            "This text appears under the header. Usually it gives brief "
            "information about the current session and has a link to "
            "submit class proposals."
        )
    )
    footer_copy = HTMLField(
        # Translators: This is the part at the end of the page.
        verbose_name=_("footer"),
        null=True,
        blank=True,
        default="Information for the footer of the page",
        help_text=_(
            "This text appears on the footer of the page. It's optional."
        )
    )

    def emails():
        def fget(self):
            try:
                return {"studentconfirmation": self.studentconfirmation,
                        "studentreminder": self.studentreminder,
                        "studentfeedback": self.studentfeedback,
                        "teacherconfirmation": self.teacherconfirmation,
                        "teacherclassapproval": self.teacherclassapproval,
                        "teacherreminder": self.teacherreminder,
                        "teacherfeedback": self.teacherfeedback
                        }
            except:
                pass
        return locals()

    emails = property(**emails())

    @property
    def domain(self):
        return Site.objects.get_current().domain

    @property
    def branch_url(self):
        """
        Url for the branch's website
        """
        return "%s%s" % (
            self.domain, reverse('course-list', kwargs={
                'branch_slug': self.slug
            })
        )

    objects = BranchManager()
    public = BranchPublicManager()
    on_site = CurrentSiteManager()

    def delete_emails(self):
        """
        Delete related emails.
        """
        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                email_obj
                email_obj.delete()

    def populate_notifications(self):
        """
        Deletes current related emails and creates new ones from the
        emails that are related to the DefulatEmailContainer object.
        """
        # delete existing emails
        self.delete_emails()

        # copy branch email from the default container's related emails
        default_email_container = DefaultEmailContainer.objects.all()[0]

        # assign the bramch to the branch attribute and save a new copy
        # of each email
        for fieldname, email_obj in default_email_container.emails.iteritems():
            new_email = copy_model_instance(email_obj)
            new_email.branch = self
            new_email.save()

    def copy_teacher_info_page(self):
        """
        Creates a copy of the teacher info flatpage for each
        new branch that gets created.
        """
        try:
            page = Page.objects.get(url='/teacher-info/', branch=None)

            page_copy = copy_model_instance(page)

            page_copy.branch = self

            page_copy.save()
        except Page.DoesNotExist:
            pass

    def generate_files(self):
        """
        Create a directory in the templates directory for the branch.
        Make a copy of all default template files.
        Create a css and javascript file for the branch.
        """
        src = settings.DEFAULT_BRANCH_TEMPLATE_DIR
        dst = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.slug)

        try:
            shutil.copytree(src, dst)
        except OSError as exc:              # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                pass

    def delete_files(self):
        """
        Delete the branch's template directory with all of the files.
        """
        directory = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.slug)

        if os.path.exists(directory):
            shutil.rmtree(directory)

    def update_template_dir(self, old_dirname, new_dirname):
        """
        Rename the branch's template directory name.
        Call this method after the branch's slug field has changed.
        """
        old_dirname = os.path.join(settings.BRANCH_TEMPLATE_DIR, old_dirname)
        new_dirname = os.path.join(settings.BRANCH_TEMPLATE_DIR, new_dirname)

        os.rename(old_dirname, new_dirname)

    def save(self, *args, **kwargs):
        """
        Check to see if the slug field's value has been changed.
        If it has, rename the branch's template dir name.

        check if status was changed to approved and create files if it has.
        """
        self.site = Site.objects.get_current()

        template_directory = os.path.join(
            settings.BRANCH_TEMPLATE_DIR,
            self.slug
        )

        if self.pk is not None and os.path.exists(template_directory):
            original = Branch.objects.get(pk=self.pk)
            if original.slug != self.slug:
                self.update_template_dir(original.slug, self.slug)

        super(Branch, self).save(*args, **kwargs)

        if self.pk is not None:
            original = Branch.objects.get(pk=self.pk)
            if original.branch_status != self.branch_status \
                    and self.branch_status != 'pending':
                self.generate_files()


class Venue(Location):
    """
    Venue represent physical locations where Trade School events take place.

    Venues are used with Course, Time, and TimeRange objects,
    but are never required.

    Attributes:
        branch: Relationship to a Branch object. Venues are always saved
            in relation to a branch.
        address_1: String indicating the street address of the venue.
        capacity: Integar indicating the number of people that the venue
            can hold. The value is not validated in the system, it's used
            for reference.
        resources: Text indicating what is available in the venue
            (like chairs, projects, etc)
        color: HTML color, currently not implemented anywhere in the system.
    """
    class Meta:
        ordering = ['branch', 'is_active', 'title']

        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _('Venue')

        # Translators: Plural
        verbose_name_plural = _('Venues')

    def random_color():
        colorValue = random.randint(0, 16777215)
        return "#%x" % colorValue

    branch = ForeignKey(
        Branch,
        verbose_name=_("branch"),
        help_text="What branch of TS is this venue related to?"
    )
    address_1 = CharField(
        max_length=200,
        verbose_name=_("Street"),
    )
    capacity = SmallIntegerField(
        max_length=4,
        default=20,
        # Translators: the capacity of the venue where you are hosting classes.
        verbose_name=_("capacity"),
        # Translators: Contextual Help
        help_text=_("How many people fit in the space?")
    )
    resources = TextField(
        # Translators: The field name for resources of a venue.
        verbose_name=_("resources"),
        null=True,
        default="For Example: Chairs, Tables",
        # Translators: Contextual Help
        help_text=_("What resources are available at the space?")
    )
    color = CharField(
        verbose_name=_("color"),
        max_length=7,
        default=random_color,
        help_text=_("A hex value HTML color in the form of #123456")
    )


class PersonManager(BaseUserManager):
    """
    Extends Django's BaseUserManager to implement a custom auth.User model.
    """
    def create_user(self, email, fullname=None, username=None, password=None, is_staff=False, **extra_fields):
        """
        Creates a Person with the given username, email and password.

        Args:
            email: The person's email address.
            fullname: the name that is used on the frontend for students
                and teachers
            username: the name that is used by organizers to log in to
                the backend.
            password: enter a password for organizers. otherwise it will
                be randomized.
            is_staff: Boolean indicating whether the person can log in
                to the backend

        Returns:
            A Person object
        """
        # ensure an email is saved
        if not email:
            raise ValueError('An email must be set')

        # create a username from the fullname
        if fullname:
            username = unique_slugify(Person, fullname, 'username')

        # set a random password when one is not entered.
        # this will happen for every saved student or teacher.
        if not password:
            password = self.make_random_password()

        # save a proper email
        email = self.normalize_email(email)

        # save a timezone-aware time
        now = timezone.now()

        person = self.model(
            email=email,
            username=username,
            fullname=fullname,
            is_staff=is_staff,
            is_active=True,
            is_superuser=False,
            last_login=now,
            **extra_fields
        )

        person.set_password(password)
        person.save(using=self._db)

        return person

    def create_superuser(self, email, password, username=None, fullname=None, **extra_fields):
        """
        Creates an admin with all permissions

        Args:
            email: The person's email address.
            password: a password for organizers.
            username: the name that is used by organizers to log in to
                the backend.
            fullname: the name that is used on the frontend for students
                and teachers

        Returns:
            A Person object
        """
        person = self.create_user(
            email,
            fullname,
            username,
            password,
            **extra_fields
        )
        person.is_staff = True
        person.is_active = True
        person.is_superuser = True
        person.save(using=self._db)
        return person

    def get_query_set(self):
        return super(
            PersonManager, self).get_query_set() \
            .select_related().prefetch_related('branches')


class Person(AbstractBaseUser, PermissionsMixin, Base):
    """
    A custom model in place of Django's auth.User model.

    A Person in the Trade School system can be an organizer,
    teacher, and student. Their interaction with the system
    determines their roles:

    When a person registers to a class, they are acknowledged as a student.
    When a person teaches an approved class, they are acknowledged as a teacher
    When a person is given is_staff=True, they are acknowledged as an organizer

    Attributes:
        fullname: String that's used to display teacher's & students' name on
            the website and in emails.
        username: String that's used by organizers to log in to the backend.
        email: String indicating the person's email.
        phone: String indicating the person's phone.
        bio: Text that's filled by teachers when submitting a class.
        website: URL that's filled by teachers when submitting a class.
        slug: URL for the person. Currently not implemented but saved.
        branches: M2M relationship to branches that the person engaged with,
            updated when a person teaches or registers to a class.
        default_branch: Foreign key to the branch that will be the default
            option for admin-related actions done by an organizer.
        language: Language code indicating the language that the admin backend
            will be translated to for an organizer.
        is_staff: Boolean indicating whether a person can log in to the backend
        courses_taught_count: The total number of approved courses taught by
            the person. Used by the Teacher proxy model.
        courses_taken_count: The total number of approved courses that the
            person was registered to. Used by the Student proxy model.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Person")

        # Translators: Plural.
        verbose_name_plural = _("People")

        ordering = ['fullname', ]

    fullname = CharField(
        max_length=200,
        verbose_name=_("your name"),
        # Translators: Contextual Help.
        help_text=_("This will appear on the site.")
    )
    username = CharField(
        max_length=200,
        unique=True,
        verbose_name=_("username"),
        help_text=_("This is used to login to the site.")
    )
    email = EmailField(
        max_length=100,
        verbose_name=_("Email address"),
        # Translators: Contextual Help.
        help_text=_("Used only for us to contact you.")
    )
    phone = CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Phone number"),
        # Translators: Contextual Help
        help_text=_("Optional. Used only for us to contact you.")
    )
    bio = TextField(
        blank=True,
        verbose_name=_("A few sentences about you"),
        # Translators: Contextual Help
        help_text=_("For prospective students to see on the website")
    )
    website = URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("Your website / blog URL"),
        # Translators: Contextual Help
        help_text=_("Optional.")
    )
    slug = SlugField(
        max_length=220,
        verbose_name=_("URL Slug"),
        help_text=_(
            "This will be used to create a unique URL "
            "for each person in TS."
        )
    )
    branches = ManyToManyField(
        Branch,
        verbose_name=_("branches"),
        # Translators: Contextual Help
        help_text=_(
            "People in the TS system can be related to many TS branches. "
            "This relationship is made when a person either teaches or "
            "registers to a class.")
    )
    default_branch = ForeignKey(
        Branch,
        verbose_name=_('default branch'),
        related_name='default_branch',
        null=True,
        blank=True,
        help_text=_(
            "This is the branch that will be selected automatically for "
            "actions this user makes. Usually the default branch is the "
            "one in which the organizer does the most work in."
        )
    )
    language = CharField(
        verbose_name=_("backend language"),
        default='en',
        max_length=50,
        choices=settings.LANGUAGES,
        null=True,
        help_text=_(
            "Setting this language will cause the admin backend to try to "
            "load text from the translation strings stored in the system "
            "FOR THIS USER ONLY. Text that wasn't translated will fallback "
            "on the English version of it."
        )
    )
    is_staff = BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        )
    )
    courses_taught_count = IntegerField(
        default=0,
        max_length=7,
        verbose_name=_("Total Classes Taught"),
        help_text=_(
            "Number of courses taught in Trade School"
        )
    )
    courses_taken_count = IntegerField(
        default=0,
        max_length=7,
        verbose_name=_("Total Classes Taken"),
        help_text=_(
            "Number of courses taken in Trade School"
        )
    )

    objects = PersonManager()

    USERNAME_FIELD = 'username'

    def branches_string(self):
        """
        Returns a comma separated string of the branches that this person
        relates to.

        This function is used in the admin list_display() method.

        Returns:
            A string joined by commas.
        """
        return ','.join(str(branch) for branch in self.branches.all())
    branches_string.short_description = _('branches')

    def branches_organized_string(self):
        """
        Returns a comma separated string of the branches that this person
        organizes.

        This function is used in the admin list_display() method.

        Returns:
            A string joined by commas.
        """
        return ','.join(
            str(branch) for branch in self.branches_organized.all()
        )
    branches_organized_string.short_description = _('branches')

    def get_full_name(self):
        """
        Retuns the person's fullname.
        Required in order to implement a replacement to django's auth.User
        """
        return self.fullname

    def get_short_name(self):
        """
        Retuns the person's fullname.
        Required in order to implement a replacement to django's auth.User
        """
        return self.fullname

    def get_absolute_url(self):
        """
        Returns a URL for the person's view page using their slug.

        The view itself is not implemented.
        Required in order to implement a replacement to django's auth.User
        """
        return '/people/%s/' % urlquote(self.slug)

    def calculate_registration_count(self):
        """
        Filters person's registrations to only count approved active courses
        that the person hasn't unregistered from.

        Used to set the courses_taken_count attribute.

        Returns:
            An integar of the total 'true' registrations.
        """
        return self.registrations.filter(
            registration_status='registered',
            course__status='approved',
            course__is_active=True,
        ).count()

    def calculate_courses_taught_count(self):
        """
        Filters person's taught courses to only count approved active courses
        that already took place.

        Used to set the courses_taught_count attribute.

        Returns:
            An integar of the total 'true' courses taught.
        """
        return self.courses_taught.filter(
            status='approved',
            start_time__lte=timezone.now(),
            is_active=True,
        ).count()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this person.

        Args:
            subject: The subject of the email.
            message: The body of the email.
            from_email: An email address to be used in the 'from' field.
        """
        send_mail(subject, message, from_email, [self.email])

    def save(self, *args, **kwargs):
        """
        Set the default_branch attribute if it's not set.
        Set courses_taken_count & courses_taught_count attributes.
        """
        self.courses_taken_count = self.calculate_registration_count()
        self.courses_taught_count = self.calculate_courses_taught_count()

        super(Person, self).save(*args, **kwargs)

        if self.default_branch is None and self.branches_organized.count() > 0:
            self.default_branch = self.branches_organized.all()[0]

    def __unicode__(self):
        """
        Return the person's fullname.
        """
        return u"%s" % self.fullname


class OrganizerManager(PersonManager):
    """
    Filter Person objects to those that have is_staff set to True.
    """
    def get_query_set(self):
        return super(
            OrganizerManager, self).get_query_set().filter(is_staff=True)


class Organizer(Person):
    """
    Organizers are Person objects that have is_staff set to True.

    Conceptually, organizers are the people who use the admin backend
    to run a chapter of Trade School and help others run theirs.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Organizer")

        # Translators: Plural.
        verbose_name_plural = _("Organizers")

        proxy = True

    objects = OrganizerManager()


class TeacherManager(PersonManager):
    """
    Filter Person objects to those who taught at least one 'true' course.
    """
    def get_query_set(self):
        return super(
            TeacherManager, self).get_query_set().filter(
                courses_taught_count__gt=0
            )


class Teacher(Person):
    """
    Teachers are Person objects that have taught at least one course.

    The distinction is made so organizers can find teacher profiles
    more easily on the admin backend. Teachers can belong to Students
    and Organizers as well.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Teacher")

        # Translators: Plural.
        verbose_name_plural = _("Teachers")

        proxy = True

    objects = TeacherManager()


class StudentManager(PersonManager):
    """
    Filter Person objects to those who take/took at least one 'true' course.
    """
    def get_query_set(self):
        return super(StudentManager, self).get_query_set().filter(
            courses_taken_count__gt=0)


class Student(Person):
    """
    Students are Person objects that are registered to least one course.

    The distinction is made so organizers can find student profiles
    more easily on the admin backend. Students can belong to Teachers
    and Organizers as well.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Student")

        # Translators: Plural.
        verbose_name_plural = _("Students")

        proxy = True

    objects = StudentManager()


class Durational(Base):
    """
    Durational is an abstract model for any model that
    has a start time and an end time.
    In the tradeschool system, these would be the Time and Course models.
    """
    class Meta:
        abstract = True

    # Translators: Used to lable the beginning and endings of classes
    start_time = DateTimeField(
        verbose_name=_("start time"),
        default=datetime.now()
    )
    # Translators: Used to lable the beginning and endings of classes
    end_time = DateTimeField(
        verbose_name=_("end time"),
        default=datetime.now()
    )


class Time(Durational):
    """
    Time is an open time slot. It is implemented in the frontend alone:
    These slots populate the calendar for teachers submitting a class.
    Times do not affect the admin class schedluing logic.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Open Time Slot")

       # Translators: Plural
        verbose_name_plural = _("Open Time Slots")

    venue = ForeignKey(
        Venue,
        verbose_name=_("venue"),
        null=True,
        blank=True,
        # Translators: Contextual Help
        help_text=_(
            "Time slots can be related to specifc venues. When "
            "a time slot that's related a venue is selected by "
            "a potential teacher, the proposed class will be booked "
            "in that venue. In the case a venue isn't selected, "
            "it's up to the organizers to select a venue for a proposed class."
        )
    )
    branch = ForeignKey(
        Branch,
        verbose_name=_("branch"),
        # Translators: Contextual Help
        help_text=_(
            "A time slot is related to a specific TS branch since it "
            "populates the times to choose from in the branch's class "
            "proposal form."
        )
    )

    def __unicode__(self):
        return u"%s" % self.start_time


class TimeRange(Base):
    """
    """
    class Meta:
        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _("Open Time Slot Batch")

        # Translators: Plural.
        verbose_name_plural = _("Open Time Slot Batches")

    start_date = DateField(
        verbose_name=_("Start date"),
        default=datetime.now(),
        help_text=_(
            "Pick the start date for the date range. "
            "The system will go over all days between this date and "
            "the end date and then create available time slots for each "
            "day of the week that you choose."
        )
    )
    end_date = DateField(
        verbose_name=_("End date"),
        default=datetime.now(),
        help_text=_(
            "Pick the start date for the date range. "
            "The system will go over all days between this date and "
            "the end date and then create available time slots for each "
            "day of the week that you choose."
        )
    )
    start_time = TimeField(
        verbose_name=_("Start time"),
        default=datetime(2008, 1, 31, 18, 00, 00),
        help_text=_(
            "This is the start time of the all of the available time slots "
            "that are going to be created."
        )
    )
    end_time = TimeField(
        verbose_name=_("End time"),
        default=datetime(2008, 1, 31, 19, 30, 00),
        help_text=_(
            "This is the end time of all of the available time slots "
            "that are going to be created."
        )
    )
    sunday = BooleanField(
        verbose_name=_("Sunday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Sundays in the above date range."
        )
    )
    monday = BooleanField(
        verbose_name=_("Monday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Mondays in the above date range."
        )
    )
    tuesday = BooleanField(
        verbose_name=_("Tuesday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Tuesdays in the above date range."
        )
    )
    wednesday = BooleanField(
        verbose_name=_("Wednesday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Wednesdays in the above date range."
        )
    )
    thursday = BooleanField(
        verbose_name=_("Thursday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Thursdays in the above date range."
        )
    )
    friday = BooleanField(
        verbose_name=_("Friday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Fridays in the above date range."
        )
    )
    saturday = BooleanField(
        verbose_name=_("Saturday"),
        help_text=_(
            "Check this day if you wish to create available times "
            "on Saturdays in the above date range."
        )
    )
    venue = ForeignKey(
        Venue,
        verbose_name=_("venue"),
        null=True,
        blank=True,
        # Translators: Contextual Help
        help_text=_(
            "All of the avaialble time slots that will be created can be "
            "related to a specifc venue. "
            "When a time slot that's related a venue is selected by "
            "a potential teacher, the proposed class will be booked in "
            "that venue. In the case a venue isn't selected, it's up to "
            "the organizers to select a venue for a proposed class."
        )
    )
    branch = ForeignKey(
        Branch,
        verbose_name=_("branch"),
        # Translators: Contextual Help
        help_text=_(
            "The available time slots will be created for this TS branch only."
        )
    )


class BarterItem(Base):
    """
    Barter items are the items that teachers request for
    a class they're teaching.
    The items themselves can be requested in various classes.
    """
    class Meta:
        ordering = ['title', ]

        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _('Barter item')

        # Translators: Plural
        verbose_name_plural = _('Barter items')

    # Translators: Wherever the barter item shows up.
    title = CharField(
        verbose_name=_("title"),
        max_length=255,
        help_text=_("A name or short description of the barter item.")
    )
    course = ForeignKey(
        'Course',
        verbose_name=_('Scheduled Class'),
        help_text=_("The scheduled class that this barter item is listed for.")
    )


class ScheduledEvent(Durational):
    """
    """
    class Meta:
        abstract = True

    STATUS_CHOICES = (
        # Translators: The thing that shows what the status of the class is
        ('pending', _('Pending')),
        ('contacted', _('Contacted')),
        ('updated', _('Updated')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected'))
    )

    COLORS = (
        ('#cc3333', 'red'),
        ('#e26521', 'blood orange'),
        ('#dda51e', 'light orange'),
        ('#74ac23', 'green'),
        ('#2da57c', 'turquoise'),
        ('#2d9ac2', 'light blue'),
        ('#8a54bb', 'violet')
    )

    title = CharField(
        max_length=255,
        verbose_name=_("class title"),
        help_text=_("The name of the class. This will appear on the website.")
    )
    branch = ForeignKey(
        Branch,
        help_text="A scheduled class is related to a TS brances. "
        "The relationship is made when a class is "
        "submitted through a specific TS branch form."
    )
    venue = ForeignKey(
        Venue,
        verbose_name=_("venue"),
        null=True,
        blank=True,
        # Translators: Contextual Help
        help_text=_("Where is this class taking place?")
    )
    students = ManyToManyField(
        Person,
        verbose_name=_("students"),
        through="Registration",
        help_text=_(
            "The students who registered to this scheduled class, "
            "what are they bringing, and whether they cancelled "
            "their attendance."
        )
    )
    description = TextField(
        blank=False,
        verbose_name=_("Class description"),
        help_text=_("The class's description. This will apear on the website.")
    )
    max_students = IntegerField(
        max_length=4,
        verbose_name=_("Maximum number of students in your class"),
        help_text=_(
            "The maximum number of students that will be able to "
            "register to this class."
        )
    )
    slug = SlugField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("A unique URL for the scheduled class.")
    )
    status = CharField(
        max_length=20,
        verbose_name=_("scheduled class status"),
        choices=STATUS_CHOICES,
        default='pending',
        # Translators: Contextual Help
        help_text=_(
            "What is the current status of the class? "
            "Only approved classes appear on the website."
        )
    )
    color = CharField(
        verbose_name=_("color"),
        choices=COLORS,
        max_length=7,
        default=random.randint(0, 6),
        help_text=_("A hex value HTML color in the form of #123456"))

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


class CourseQuerySet(QuerySet):
    def pending(self):
        return self.filter(end_time__gte=timezone.now()) \
            .exclude(status='approved') \
            .exclude(status='rejected')

    def approved(self):
        return self.filter(
            status='approved',
            end_time__gte=timezone.now()
        )

    def past(self):
        return self.filter(end_time__lte=timezone.now())

    def public(self):
        return self.filter(is_active=True, status='approved')


class CourseManager(Manager):
    def get_query_set(self):
        return CourseQuerySet(self.model, using=self._db).select_related(
            'venue__title',
            'title',
            'description',
            'max_students',
            'teacher__fullname',
            'teacher__email',
            'teacher__phone',
            'teacher__website',
            'teacher__bio',
            'studentconfirmation',
            'studentreminder',
            'studentfeedback',
            'teacherconfirmation',
            'teacherclassapproval',
            'teacherreminder',
            'teacherfeedback',
        )

    def pending(self):
        return self.get_query_set().pending()

    def approved(self):
        return self.get_query_set().approved()

    def past(self):
        return self.get_query_set().past()

    def public(self):
        return self.get_query_set().public()


class Course(ScheduledEvent):
    """
    """
    class Meta:
        # Translators: Any times that the word class is shown as singular
        verbose_name = _("Class")

        # Translators: Any times that the word class is shown as plural
        verbose_name_plural = _("Classes")

        ordering = ['status', 'start_time', '-venue', 'title']

    teacher = ForeignKey(
        Person,
        verbose_name=_("teacher"),
        related_name='courses_taught',
        help_text=_("The person teaching this class.")
    )

    def emails():
        def fget(self):
            try:
                return {"studentconfirmation": self.studentconfirmation,
                        "studentreminder": self.studentreminder,
                        "studentfeedback": self.studentfeedback,
                        "teacherconfirmation": self.teacherconfirmation,
                        "teacherclassapproval": self.teacherclassapproval,
                        "teacherreminder": self.teacherreminder,
                        "teacherfeedback": self.teacherfeedback
                        }
            except:
                pass
        return locals()

    emails = property(**emails())

    @property
    def student_feedback_url(self):
        """
        url for students to leave feedback for a scheduled class
        """
        return "%s%s" % (
            self.branch.domain, reverse('course-feedback', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
                'feedback_type': 'student'
            })
        )

    @property
    def teacher_feedback_url(self):
        """
        url for teachers to leave feedback for a scheduled class
        """
        return "%s%s" % (
            self.branch.domain, reverse('course-feedback', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
                'feedback_type': 'teacher'
            })
        )

    @property
    def course_edit_url(self):
        """
        Url for teachers to edit a scheduled class.
        """
        return "%s%s" % (
            self.branch.domain, reverse('course-edit', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
            })
        )

    objects = CourseManager()

    def registered_students(self):
        return self.registration_set.registered().count()

    def student_list_string(self):
        """
        create a string with the registered students for a scheduled class.
        """
        student_list = ""
        for registration_obj in self.registration_set.registered():
            student_list += "\n%s: " % registration_obj.student.fullname
            student_items = []
            for item in registration_obj.items.all():
                student_items.append(item.title)
            student_list += ", ".join(map(str, student_items))

        return student_list

    def delete_emails(self):
        # delete existing  emails
        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                email_obj
                email_obj.delete()

    def populate_notifications(self):
        """
        resets course notification templates from
        the branch notification templates
        """
        # delete existing branch emails
        self.delete_emails()

        # copy course notification from the branch notification templates
        for fieldname, email_obj in self.branch.emails.iteritems():
            new_email = copy_model_instance(email_obj)
            new_email.pk = None
            new_email.branch = None
            if isinstance(new_email, TimedEmail):
                new_email.set_send_on(self.start_time)
            new_email.course = self
            new_email.save()

    def approve_courses(self, request, queryset):
        "approve multiple courses"
        rows_updated = queryset.update(status='approved')
        if rows_updated == 1:
            message_bit = "1 class was"
        else:
            message_bit = "%s classes were" % rows_updated
            self.message_user(
                request, "%s successfully approved." % message_bit)
    approve_courses.short_description = "Approve Classes"

    def send_timed_emails_in_range(self, start_date, end_date):
        """
        """
        email_count = 0

        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                if isinstance(email_obj, TimedEmail):

                    # check if email send on is within range & was not sent yet
                    if start_date < email_obj.send_on < end_date \
                            and email_obj.email_status == 'not_sent':

                        # email students
                        if isinstance(email_obj, StudentReminder):
                            email_count += self.email_students(
                                self.studentreminder)

                        if isinstance(email_obj, StudentFeedback):
                            email_count += self.email_students(
                                self.studentfeedback)

                        # email teacher
                        if isinstance(email_obj, TeacherReminder):
                            self.email_teacher(self.teacherreminder)
                            email_count += 1

                        if isinstance(email_obj, TeacherFeedback):
                            self.email_teacher(self.teacherfeedback)
                            email_count += 1

        # if there is no CourseEmailContainer,
        # populate new emails for the Course
        else:
            self.populate_notifications()

        return email_count

    def generate_barteritems_from_past_course(self):
        """
        Find a past Course of the same Course
        and copy its BarterItem objects.
        """

        # find a scheduled course to this Course's course,
        # which is not this one
        past_courses = Course.objects.exclude(pk=self.pk)

        if past_courses.exists():

            # create copies of the past course's BarterItem objects.
            # reset the pk for each one so a new object is saved,
            # and create a relationship to the current Course.
            for item in past_courses[0].barteritem_set.all():
                new_item = copy_model_instance(item)
                new_item.pk = None
                new_item.course = self
                new_item.save()

    def email_teacher(self, email):
        """shortcut method to send an email via the Course object."""
        return email.send(self, (self.teacher.email,))

    def email_student(self, email, registration):
        """shortcut method to send an email via the Course object."""
        return email.send(self, (registration.student.email,), registration)

    def email_students(self, email):
        """shortcut method to send an email via the Course object."""
        email_count = 0
        for registration in self.registration_set.registered():
            self.email_student(email, registration)
            email_count += 1
        return email_count

    def save(self, *args, **kwargs):
        """
        check if status was changed to approved and email teacher if it has.
        """
        # generate and save slug if there isn't one
        if self.slug is None or self.slug.__len__() == 0:
            self.slug = unique_slugify(Course, self.title)

        if self.pk is not None:
            try:
                original = Course.objects.get(pk=self.pk)

                if original.status != self.status \
                        and self.status == 'approved':

                    self.email_teacher(self.teacherclassapproval)
            except Course.DoesNotExist:
                pass

        # call the super class's save method
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % (self.title)


class PendingCourseManager(CourseManager):
    def get_query_set(self):
        return super(PendingCourseManager, self).get_query_set().pending()


class PendingCourse(Course):
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Scheduled Class: Pending")

        # Translators: Plural.
        verbose_name_plural = _("Scheduled Classes: Pending")

        proxy = True

    objects = PendingCourseManager()


class ApprovedCourseManager(CourseManager):
    def get_query_set(self):
        return super(ApprovedCourseManager, self).get_query_set().approved()


class ApprovedCoursePublicManager(ApprovedCourseManager):
    def get_query_set(self):
        return super(
            ApprovedCoursePublicManager, self) \
            .get_query_set().approved().public()


class ApprovedCourse(Course):
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Scheduled Class: Approved")

        # Translators: Plural.
        verbose_name_plural = _("Scheduled Classes: Approved")

        proxy = True

    objects = ApprovedCourseManager()
    public = ApprovedCoursePublicManager()


class PastCourseManager(CourseManager):
    def get_query_set(self):
        return super(PastCourseManager, self).get_query_set().past()


class PastCoursePublicManager(PastCourseManager):
    def get_query_set(self):
        return super(
            PastCoursePublicManager, self).get_query_set().past().public()


class PastCourse(Course):
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Scheduled Class: Past")

        # Translators: Plural.
        verbose_name_plural = _("Scheduled Classes: Past")

        ordering = ['-start_time', '-venue']

        proxy = True

    objects = PastCourseManager()    
    public = PastCoursePublicManager()


class RegistrationQuerySet(QuerySet):
    def registered(self):
        return self.filter(registration_status='registered')


class RegistrationManager(Manager):
    def get_query_set(self):
        return RegistrationQuerySet(self.model, using=self._db).select_related(
            'course',
            'student',
            'student__fullname',
            'items__title'
        ).prefetch_related('items')

    def registered(self):
        return self.get_query_set().registered()


class Registration(Base):
    """
    Registrations represent connections between students and classes.
    When a student registers to a class a registration row is added.
    We do this because we also want to keep track of students who registered
    and then unregistered from a class.
    """
    class Meta:
        unique_together = ('course', 'student')
        ordering = [
            '-course__start_time',
            'course',
            'registration_status',
            'student'
        ]

        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _('Registration')

        # Translators: Plural
        verbose_name_plural = _('Registrations')

    # Translators: Student registration buttons.
    REGISTRATION_CHOICES = (('registered', _('Registered')),
                            ('unregistered', _('Unregistereed')))

    course = ForeignKey(
        Course,
        verbose_name=_("course"),
        help_text=_("What scheduled class does this registration refer to?")
    )
    student = ForeignKey(
        Person,
        verbose_name=_("student"),
        related_name='registrations',
        help_text=_("Who registered?")
    )
    registration_status = CharField(
        verbose_name=_("registration status"),
        max_length=20,
        choices=REGISTRATION_CHOICES,
        default='registered',
        help_text=_("Did the student cancel?")
    )
    items = ManyToManyField(
        BarterItem,
        verbose_name=_("items"),
        blank=False,
        help_text=_(
            "The barter items that the student said "
            "they were bringing to the class."
        )
    )

    @property
    def unregister_url(self):
        """
        Url for student to unregister from a scheduled class.
        """
        domain = self.course.branch.domain

        return "%s%s" % (
            domain, reverse('course-unregister', kwargs={
                'branch_slug': self.course.branch.slug,
                'course_slug': self.course.slug,
                'student_slug': self.student.slug
            })
        )

    objects = RegistrationManager()

    def registered_item_string(self):
        """
        create a string with the items the student registered to bring.
        Used in emails for students.
        """
        item_list = ""
        for item in self.items.all():
            item_list += "%s\n" % item.title

        return item_list

    def registered_items(self):
        """ Return the registered items as a string. Used in the admin."""
        return ','.join(str(item) for item in self.items.all())

    def __unicode__(self):
        return "%s: %s" % (self.student, self.registration_status)


class Feedback(Base):
    """
    Feedback is collected after courses take place.
    """
    class Meta:
        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _('Feedback')

        # Translators: Plural
        verbose_name_plural = _('Feedbacks')

    # Translations: These next three are for the feedback form.
    FEEDBACK_TYPE_CHOICES = (
        ('teacher', _('From the Teacher')),
        ('student', _('From a student'))
    )

    course = ForeignKey(
        Course,
        verbose_name=_("course"),
        help_text=_(
            "Feedback is given for a class that was scheduled and took place."
        )
    )
    feedback_type = CharField(
        verbose_name=_("feedback type"),
        max_length=20,
        choices=FEEDBACK_TYPE_CHOICES,
        default='student',
        help_text=_(
            "Was this feedback given by a student in the class "
            "or by the teacher?"
        )
    )
    # Translators: Contextual Help
    content = TextField(
        help_text=_("your feedback"),
        verbose_name=_('Your Feedback')
    )

    def __unicode__(self):
        return u'%s: feedback %s' % (
            self.course.title, self.feedback_type)


class Photo(Base):
    """
    Each branch has photos that can go in a gallery
    """
    class Meta:
        ordering = ['position', ]

        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _('Photo')

        # Translators: Plural
        verbose_name_plural = _('Photos')

    def upload_path(self, filename):
        return "uploads/%s/images/%s" % (self.branch.slug, filename)

    # Translators: These next three are for the photograph files
    filename = ImageField(
        _("Photo"),
        upload_to=upload_path
    )
    position = PositiveSmallIntegerField(
        _('Position'),
        default=0,
        help_text=_(
            "This indicates the order in which the pictures "
            "appear on the website."
        )
    )
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

    def __unicode__(self):
        return "%s: %s" % (self.branch.title, self.filename)


class PageQuerySet(QuerySet):
    def public(self):
        return self.filter(is_active=True)

    def visible(self):
        return self.filter(is_visible=True)


class PageManager(Manager):
    def get_query_set(self):
        return PageQuerySet(self.model, using=self._db)

    def public(self):
        return self.get_query_set().public()

    def visible(self):
        return self.get_query_set().visible()


class Page(Base):
    """Extending the FlatPage model to provide branch-specific content pages.
    """
    class Meta:
        ordering = ['branch', 'title']

        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _('Branch Page')

        # Translators: Plural
        verbose_name_plural = _('Branch Pages')

        unique_together = ('branch', 'url')

    url = CharField(
        verbose_name=_('URL'),
        max_length=100,
        db_index=True
    )
    title = CharField(
        verbose_name=_('title'),
        max_length=200
    )
    content = HTMLField(
        verbose_name=_('content'),
        blank=True
    )
    # Translators: Determines whether a page is shown on  menu or not.
    is_visible = BooleanField(
        verbose_name=_("is visible"),
        default=1,
        help_text=_(
            "This indicates whether a page is listed in the menu or not. "
            "Visible pages appear on the menu. Other pages do not, "
            "but are still accessible via their URL."
        )
    )
    # Translators: These one is for the dynamic custom pages.
    branch = ForeignKey(
        Branch,
        verbose_name=_("branch"),
        null=True,
        blank=True
    )
    position = PositiveSmallIntegerField(
        _('Position'),
        default=0,
        help_text=_(
            "This indicates the order in which the pages are listed "
            "in the menu."
        )
    )

    objects = PageManager()

# signals are separated to signals.py
# just for the sake of organization
import signals
