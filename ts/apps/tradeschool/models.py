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
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail
from django.core.mail import EmailMessage
#from django_mailer import send_mail
from django.template import Context
from django.template import Template
from django_countries.fields import CountryField
from tinymce.models import HTMLField
from datetime import *
from tradeschool.utils import copy_model_instance, unique_slugify


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
        ('not_sent', _('Enabled (Not Sent Yet)')),

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
        # turn autoescape off in the template
        tz_tag = '{% timezone "' + course_obj.branch.timezone + '" %}'

        content_with_tag = '{% load tz %}' + tz_tag + '{% autoescape off %}' + self.content + '{% endautoescape %} {% endtimezone %}'

        # instantiate a temlate with the email's content
        template = Template(content_with_tag)

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
        message = EmailMessage(
            subject=self.subject,
            body=body,
            to=recipient,
            headers={'Reply-To': branch.email}
        )
        message.send()

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

    phone = CharField(
        verbose_name=_("phone"),
        max_length=30,
        blank=True,
        null=True,
        # Transalators: Contextual Help.
        help_text=_("Optional.")
    )
    city = CharField(
        verbose_name=_("City/Province/Region"),
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

    def __unicode__(self):
        """
        Returns: a unicode string of the Cluster's name attribute.
        """
        return u"%s" % self.name


class Language(Base):
    """
    A database representation of a language that's in django.settings.

    It's redundant to duplicate this data, but this is how branches can
    use more than one language.

    Attributes:
        code: String indicating the language code as it's defined in settings
        branches: M2M to the Branches that use this language.
        position: Integar indicating the index of the image in the slideshow.
    """
    class Meta:
        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _('Language')

        # Translators: Plural
        verbose_name_plural = _('Languages')

    code = CharField(
        verbose_name=_('Name'),
        max_length=6,
        choices=settings.LANGUAGES,
        db_index=True
    )

    def __unicode__(self):
        return u'%s' % dict(settings.LANGUAGES).get(self.code)


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
    common_timezones = [tz for tz in pytz.all_timezones if 'GMT' in tz]

    COMMON_TIMEZONE_CHOICES = tuple(
        zip(common_timezones, common_timezones)
    )

    title = CharField(
        # Translators: This is for the name of a Trade School location or venue
        verbose_name=_("title"),
        max_length=100,
        unique=True,
        # Translators: Contextual Help.
        help_text=_("The name of the school")
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
        default='Etc/GMT+0',
        help_text=_(
            "The local timezone in the area where this branch of TS"
            "is taking place. The timezone is used to calculate all "
            "the class and email times."
        )
    )
    language = CharField(
        verbose_name=_("default language"),
        max_length=50,
        choices=settings.LANGUAGES,
        null=True,
        default='en',
        help_text=_(
            "Setting this language will cause both the front end and "
            "the backend of the site to try to load text from the translation "
            "strings stored in the system. Text that wasn't translated will "
            "fallback on the English version of it."
        )
    )
    languages = ManyToManyField(
        Language,
        verbose_name=_("languagaes"),
        help_text=_(
            "Select multiple languages that you would like the site to be "
            "displayed in."
        ),
        null=True,
        blank=True
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
    google_analytics_code = TextField(
        # Translators: This is the part at the end of the page.
        verbose_name=_("Google Analytics Code"),
        null=True,
        blank=True,
        help_text=_(
            "Paste in the tracking code from Google Analytics here "
            "if you want to track all of the branch's pages."
        )
    )
    min_barteritems = PositiveSmallIntegerField(
        verbose_name=_("Minimum Barter Items for each class"),
        null=False,
        blank=False,
        default=5,
        help_text=_(
            "The minimum number of barter items a teacher need to list "
            "when submitting a class on the website."
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
        return "http://%s%s" % (
            self.domain, reverse_lazy('course-list', kwargs={
                'branch_slug': self.slug
            })
        )

    objects = BranchManager()
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

    def add_support_orgazniers(self):
        """
        Add all Organizers with is_giving_support status
        as orgazniers of the Branch.
        """
        for organizer in Organizer.objects.filter(
                is_giving_support=True, is_active=True):
            self.organizers.add(organizer)

    def email_support_users(self):
        """
        Send an email to all organizers with is_giving_support=True
        to notify them about the new branch that was created
        """
        subject = "Trade School Everywhere | New pending branch: %s" % self.title

        base_url = "http://%s" % self.domain
        branch_url = base_url  + reverse('admin:tradeschool_pendingbranch_change',  args=[self.pk])

        body = """
        Hello, this is the Trade School website emailing you!\n
        Someone wants to open a new school in %s %s %s\n
        See more details at %s\n.
        Thank you!
        """ % (self.city, self.state, self.country.name, branch_url)

        recipients = Organizer.objects.filter(
            is_giving_support=True).values_list('email', flat=True)

        message = EmailMessage(
            subject=subject,
            body=body,
            to=recipients
        )
        message.send()

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
            try:
                original = Branch.objects.get(pk=self.pk)
                if original.slug != self.slug:
                    self.update_template_dir(original.slug, self.slug)
            except Branch.DoesNotExist:
                pass

        super(Branch, self).save(*args, **kwargs)

        if self.pk is not None:
            try:
                original = Branch.objects.get(pk=self.pk)
                if original.branch_status != self.branch_status \
                        and self.branch_status != 'pending':
                    self.generate_files()
            except Branch.DoesNotExist:
                pass


class PendingBranchManager(BranchManager):
    """
    Filter Branch objects to those that have branch_status set to 'pending'.
    """
    def get_query_set(self):
        return super(
            PendingBranchManager, self).get_query_set().filter(
                branch_status='pending')


class PendingBranch(Branch):
    """
    Pending Branches are Branch objects that have branch_status set to pending.

    Conceptually, pending branches are the result of the start a trade school
    form.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Pending Branch")

        # Translators: Plural.
        verbose_name_plural = _("Pending Branches")

        proxy = True

    objects = PendingBranchManager()


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

    title = CharField(
        # Translators: This is for the name of a Trade School location or venue
        verbose_name=_("title"),
        max_length=100,
        # Translators: Contextual Help.
        help_text=_("The name of the space")
    )
    branch = ForeignKey(
        Branch,
        verbose_name=_("branch"),
        help_text=_("What branch of TS is this venue related to?")
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
    directions = TextField(
        verbose_name=_("Directions"),
        null=True,
        blank=True,
        help_text=_(
            "Include directions for getting to the space, parking "
            "information, etc"
        )
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
    is_giving_support = BooleanField(
        _('Trade School Everywhere status'),
        default=False,
        help_text=_(
            "Designates whether the user supports "
            "other organizers through the backend."
        )
    )
    is_teacher = BooleanField(
        _('teacher status'),
        default=False,
        help_text=_(
            "Designates whether the user is considered a teacher on the site."
        )
    )
    is_student = BooleanField(
        _('student status'),
        default=True,
        help_text=_(
            "Designates whether the user is considered a student on the site."
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
    names_of_co_organizers = CharField(
        max_length=50,
        verbose_name=_("names of co-organizers"),
        null=True,
        blank=True
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
        if self.courses_taken_count > 0:
            self.is_student = True
        self.courses_taught_count = self.calculate_courses_taught_count()
        if self.courses_taught_count > 0:
            self.is_teacher = True

        super(Person, self).save(*args, **kwargs)

        if self.default_branch is None and self.branches_organized.count() > 0:
            self.default_branch = self.branches_organized.all()[0]

        if self.default_branch is not None \
                and self.branches_organized.count() == 0:
            self.branches_organized.add(self.default_branch)

    def __unicode__(self):
        """
        Return the person's fullname.
        """
        return u"%s" % self.username


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
            TeacherManager, self).get_query_set().filter(is_teacher=True)


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
            is_student=True)


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
    Durational is an abstract model that has a start time and an end time.

    Time and ScheduledEvent extend this model.

    Attributes:
        start_time: Datetime indicating the beginning of the event.
        end_time: Datetime indicating the end of the event.
    """
    class Meta:
        abstract = True

    # Translators: Used to label the beginning and endings of classes
    start_time = DateTimeField(
        verbose_name=_("start time"),
        default=datetime.now()
    )
    # Translators: Used to label the beginning and endings of classes
    end_time = DateTimeField(
        verbose_name=_("end time"),
        default=datetime.now()
    )


class Time(Durational):
    """
    A time slot that can be selected by teachers when submitting a course.

    The Time model is implemented in the frontend alone:
    These slots populate the class submission form that teachers use when
    submitting a class.

    After a class was submitted by a teacher using the class submission form,
    the time that was selected will be deleted and will no longer be available.

    The selected time is NOT bound to the course, and can be edited by
    the organizers.

    Attributes:
        venue: Foreign key to a Venue object. If the open time is related to
            the availability of a location, saving a venue with the time will
            ensure that the venue is saved to the submitted course.
        branch: Foreign key to a Branch. Time slots are specific to a branch
            since they are used in each branch's class submission form.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("One Time Slot")

       # Translators: Plural
        verbose_name_plural = _("One Time Slot")

    venue = ForeignKey(
        Venue,
        on_delete=SET_NULL,
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
        """
        Return the start time.
        """
        return u"%s" % self.start_time


class TimeRange(Base):
    """
    A range of dates, used to create multiple Time objects in a batch.

    An organizer indicates the start and end time of each time slot they
    want created within a date range. They check off the days in which times
    should be created.

    When a TimeRange is saved, individual Time objects within the set range
    are saved individually. They can then be edited/saved/deleted individually.

    When a TimeRange is deleted, the Time objects within the set range
    are deleted.

    Attributes:
        start_date: Date indicating start date of the date range.
        end_date: Date indicating the end date of the date range.
        start_time: Time indicating the start time of each saved Time object.
        end_time: Time indicating the end time of each saved Time object.
        sunday: Boolean indicating whether to create Time slots for Sundays.
        monday: Boolean indicating whether to create Time slots for Mondays.
        tuesday: Boolean indicating whether to create Time slots for Tuesdays.
        wednesday: Boolean indicating whether to create Time slots for
            Wednesdays.
        thursday: Boolean indicating whether to create Time slots for Thursday.
        friday: Boolean indicating whether to create Time slots for Fridays.
        saturday: Boolean indicating whether to create Time slots for
            Saturdays.
        venue: Foreign key to a Venue object. If the times are related to
            the availability of a location, saving a venue with the time will
            ensure that the venue is saved to each saved time.
        branch: Foreign key to a Branch. Time slots are specific to a branch
            since they are used in each branch's class submission form.
    """
    class Meta:
        # Translators: This is used in the header navigation
        #  to let you know where you are.
        verbose_name = _("Many Time Slots")

        # Translators: Plural.
        verbose_name_plural = _("Many Time Slots")

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
        default=datetime(2008, 1, 31, 8, 00, 00),
        help_text=_(
            "This is the start time of the all of the available time slots "
            "that are going to be created."
        )
    )
    end_time = TimeField(
        verbose_name=_("End time"),
        default=datetime(2008, 1, 31, 10, 00, 00),
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
        on_delete=SET_NULL,
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
    Barter items are requested by teachers when submitting a course
    and are selected by students registering to a course.
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
    An abstract class that events in the Trade School system inherits from.
    A Course is a ScheduledEvent.

    Attributes:
        title: String indicating the name of the event.
        branch: Foreign key to a Branch that this event is related to.
        venue: Foreign key to a Venue that this event is scheduled
            to take place in
        students: M2M relationship with the people who are registered
            to the event.
        description: Textual description of the event.
        max_students: Integar of the maximum number of people who can register.
        slug: URL slug that is used to create a view page for the event.
        status: String indicating whether the event is proposed or approved
            by the organizers of the Branch.
        color: HTML color that will be used to style the event on the website.
        is_within_a_day: Boolean indicating whether the event is scheduled
            to start in the next day.
        is_past: Boolean indicating whether the event already took place.
    """
    class Meta:
        abstract = True

    STATUS_CHOICES = (
        # Translators: The thing that shows what the status of the class is
        ('pending', _('Pending')),
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
        ('#8a54bb', 'violet'),
        ('#CCCCFF', 'lavender'),
        ('#989898', 'grey'),
        ('#FFFF66', 'yellow'),
        ('#99FFCC', 'seafoam'),
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
        on_delete=SET_NULL,
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
        """
        Indicating whether the event is scheduled to start in the next day.
        """
        if (self.start_time - timezone.now()) < timedelta(hours=24):
            return True
        return False

    @property
    def is_past(self):
        """
        Indicating whether the event already took place.
        """
        if self.end_time < timezone.now():
            return True
        return False


class CourseQuerySet(QuerySet):
    """
    Defines querysets for pending, approved, past, and public courses.
    """
    def pending(self):
        """
        Returns courses that were not approved.
        """
        return self.filter(end_time__gte=timezone.now()) \
            .exclude(status='approved') \
            .exclude(status='rejected')

    def approved(self):
        """
        Returns courses that were approved but haven't taken place yet.
        """
        return self.filter(
            status='approved',
            end_time__gte=timezone.now()
        )

    def past(self):
        """
        Returns courses that already took place.
        """
        return self.filter(end_time__lte=timezone.now())

    def rejected(self):
        """
        Returns courses that were rejected.
        """
        return self.filter(status='rejected')

    def public(self):
        """
        Returns active courses that were approved.
        """
        return self.filter(is_active=True, status='approved')


class CourseManager(Manager):
    """
    A Manager selecting related emails and teacher attributes.
    """
    def get_query_set(self):
        """
        Selects related Email objects, venue, and teacher attributes from
        the custom QuerySet.
        """
        return CourseQuerySet(self.model, using=self._db).select_related(
            'venue__title',
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

    def rejected(self):
        return self.get_query_set().rejected()

    def public(self):
        return self.get_query_set().public()


class Course(ScheduledEvent):
    """
    A one time scheduled class that is taught by a teacher in a TS Branch.

    Course is currently the main model that Trade School facilitates:

    A teacher submits a class proposal through the frontend class submission
    form on a branch's website. The proposal includes the attributes of a
    ScheduledEvent model, a list of barter items and the teacher's information.
    The class proposal is either approved or not by the branch's organizers.
    Approved courses appear on the branch's website so students can register
    to them. Students register by agreeing to bring one or more of the items
    that were requested by the teacher.

    A Course also has 7 types of emails that are sent automatically:
        teacherconfirmation: Sent to the teacher to confirm a successful
            course submission. Also includes a link to edit the course.
        teacherclassapproval: Sent to the teacher to notify them the course
            was approved by the organizers.
        studentreminder: Sent to a student to confirm a successful course
            registration.
        studentconfirmation: Sent to all registered students before the course
            is scheduled to start to remind them it's happening and what items
            they said they would bring. It also includes a link to unregister.
        teacherreminder: Sent to the teacher before the course is scheduled
            to start to remind them that it's happening.
        teacherfeedback: Sent to a teacher after the course took place with
            a link to leave feedback.
        studentfeedback: Sent to all registered students after the course took
            place with a link to leave feedback.

    Attributes:
        teacher: Foreign key to the teacher who submitted the class.
        emails: Dictionary with all of the related Email objects.
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
    total_registered_students = IntegerField(
        verbose_name=_("Total Registered Students"),
        default=0,
        help_text=_(
            "The number of students who are currently registered to the class"
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
    def student_feedback_url(self):
        """
        Returns URL for students to leave feedback for a scheduled class.
        """
        return "http://%s%s" % (
            self.branch.domain, reverse_lazy('course-feedback', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
                'feedback_type': 'student'
            })
        )

    @property
    def teacher_feedback_url(self):
        """
        Returns URL for teachers to leave feedback for a scheduled class.
        """
        return "http://%s%s" % (
            self.branch.domain, reverse_lazy('course-feedback', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
                'feedback_type': 'teacher'
            })
        )

    @property
    def course_edit_url(self):
        """
        Returns URL for teachers to edit a scheduled class.
        """
        return "http://%s%s/" % (
            self.branch.domain, reverse_lazy('course-edit', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
            })
        )

    @property
    def course_view_url(self):
        """
        Returns the URL for viewing the details about a scheduled class.
        """
        return "http://%s%s" % (
            self.branch.domain,
            reverse_lazy('course-view', kwargs={
                'branch_slug': self.branch.slug,
                'course_slug': self.slug,
            })
        )

    @property
    def is_past(self):
        """
        Returns True if the course would be a PastCourse.
        """
        if self.end_time < timezone.now():
            return True
        else:
            return False

    @property
    def is_almost_full(self):
        """
        Returns True if the course has 3/4 registrations
        """
        if float(self.total_registered_students) / float(self.max_students) >= 0.75 \
                and self.total_registered_students < self.max_students:
            return True
        else:
            return False

    objects = CourseManager()

    def set_registered_students(self):
        """
        Sets the total registration count
        """
        self.total_registered_students = self.registration_set.registered().count()
        self.save()

    def student_list_string(self):
        """
        Creates a string with the registered students for a scheduled class.

        Returns:
            A string of students and the items they registered to bring.
        """
        student_list = ""
        for registration_obj in self.registration_set.registered():
            student_list += "\n%s: " % unicode(registration_obj.student.fullname)
            student_items = []
            for item in registration_obj.items.all():
                student_items.append(unicode(item.title))
            student_list += ", ".join(map(unicode, student_items))

        return student_list

    def delete_emails(self):
        """
        Delete existing related Email objects.
        """
        if self.emails is not None:
            for fieldname, email_obj in self.emails.iteritems():
                email_obj
                email_obj.delete()

    def populate_notifications(self):
        """
        Resets the Course Email objects.

        The emails are copied from the Email objects that
        are related to the Branch that the course is related to.
        """
        # delete the existing course related emails
        self.delete_emails()

        # copy course emails from the related branch emails
        for fieldname, email_obj in self.branch.emails.iteritems():

            # create a copy of the email object
            new_email = copy_model_instance(email_obj)

            # make sure not to save over the original row
            # a new pk will be created
            new_email.pk = None

            # remove the relationship between the email and the branch
            new_email.branch = None

            # check if this email is a timed email that needs extra setup
            if isinstance(new_email, TimedEmail):
                new_email.set_send_on(self.start_time)

            # relate the email to this course
            new_email.course = self

            # finally, save!
            new_email.save()

    def approve_courses(self, request, queryset):
        """
        Approve multiple Course objects.
        Implemented as an admin action.
        """
        # change status to 'approved'
        rows_updated = queryset.update(status='approved')

        # format a nice grammatically correct message
        if rows_updated == 1:
            message_bit = "1 class was"
        else:
            message_bit = "%s classes were" % rows_updated
            self.message_user(
                request, "%s successfully approved." % message_bit)
    approve_courses.short_description = "Approve Classes"

    def send_timed_emails_in_range(self, start_date, end_date):
        """
        Email any related TimedEmail objects that are in the given date range.

        These emails can be: student reminder, teacher reminder,
        student feedback, and teacher feedback.

        A count of the emails that were sent is kept for a unittest.

        Args:
            start_date: Date indicating the start of the date range.
            end_date: Date indicating the end of the date range.

        Returns:
            Integar of the total emails that were sent.
        """
        email_count = 0

        # first make sure that the course has related emails
        if self.emails is None:

            # create emails for the course
            self.populate_notifications()

        # iterate over course emails
        for fieldname, email_obj in self.emails.iteritems():

            # only pay attention to emails that are scheduled to be sent
            # automatically by the system at a certain time.
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

        return email_count

    def copy_barteritems_from_course(self, course):
        """
        Copy BarterItem objects that are related to a course
        and assign them to this course.

        This is used when creating a copy of a Course for a repeat class.

        Args:
            course: Course object to copy barter items from.
        """
        for item in course.barteritem_set.all():

            # create a copy of the course's barter item
            new_item = copy_model_instance(item)

            # reset the pk for each one so a new object is saved,
            new_item.pk = None

            # create a relationship to the current Course.
            new_item.course = self

            # save
            new_item.save()

    def email_teacher(self, email):
        """
        Shortcut method that emails the course's teacher via the Course object.

        Args:
            email: Email object that will be sent
                (along with its subject, body, etc )
        """
        return email.send(self, (self.teacher.email,))

    def email_student(self, email, registration):
        """
        Shortcut method that emails a student via the Course object.

        Args:
            email: Email object that will be sent
                (along with its subject, body, etc )
            registration: Registration object that is used to populate
                the email content.
        """
        return email.send(self, (registration.student.email,), registration)

    def email_students(self, email):
        """
        Shortcut method that emails all registered students via
        the Course object.

        Args:
            email: Email object that will be sent
                (along with its subject, body, etc )

        A count of the emails that were sent is kept for a unittest.

        Returns:
            Integar of the total emails that were sent.
        """
        email_count = 0

        # iterate over registered students (excludes unregistered students)
        for registration in self.registration_set.registered():
            self.email_student(email, registration)
            email_count += 1

        return email_count

    def save(self, *args, **kwargs):
        """
        Generates slug if it does not exist.
        Emails teacher if it the status was changed to 'approved'
        """
        # generate and save slug if there isn't one
        if self.slug is None or self.slug.__len__() == 0:
            self.slug = unique_slugify(Course, self.title)

        # if this is not the first time the object is saved
        if self.pk is not None:
            try:
                # keep the pre-saved values in a variable
                original = Course.objects.get(pk=self.pk)

                # compare the pre-saved status with the current status
                if original.status != self.status \
                        and self.status == 'approved':

                    # email teacher if the course was approved to let them know
                    self.email_teacher(self.teacherclassapproval)

                # compare the pre-saved status with the current status
                if original.status != self.status \
                        and self.status == 'rejected':

                    # recreate the time slot
                    time = Time(
                        start_time=self.start_time,
                        end_time=self.end_time,
                        venue=self.venue,
                        branch=self.branch
                    )
                    time.save()

            except Course.DoesNotExist:
                pass

        # call the super class's save method
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        """
        Returns the course's title.
        """
        return "%s" % (self.title)


class PendingCourseManager(CourseManager):
    """
    Filter Course objects to those that have status set to 'pending'.
    """
    def get_query_set(self):
        return super(PendingCourseManager, self).get_query_set().pending()


class PendingCourse(Course):
    """
    Pending courses are Course objects that were submitted but not approved yet

    Pending courses are only visible to organizers on the admin backend.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Class: Pending")

        # Translators: Plural.
        verbose_name_plural = _("Classes: Pending")

        proxy = True

    objects = PendingCourseManager()


class ApprovedCourseManager(CourseManager):
    """
    Filter Course objects to those that have status set to 'approved'.
    """
    def get_query_set(self):
        return super(ApprovedCourseManager, self).get_query_set().approved()


class ApprovedCoursePublicManager(ApprovedCourseManager):
    """
    Filter Course objects to approved courses that should appear on the website
    """
    def get_query_set(self):
        return super(
            ApprovedCoursePublicManager, self) \
            .get_query_set().approved().public()


class ApprovedCourse(Course):
    """
    Pending courses are Course objects that were approved by an organizer.

    Approved course appears on the branch's website and students can
    register to it.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Class: Approved")

        # Translators: Plural.
        verbose_name_plural = _("Classes: Approved")

        proxy = True

    objects = ApprovedCourseManager()
    public = ApprovedCoursePublicManager()


class PastCourseManager(CourseManager):
    """
    Filter Course objects to those that already took place.
    """
    def get_query_set(self):
        return super(PastCourseManager, self).get_query_set().past()


class PastCoursePublicManager(PastCourseManager):
    """
    Filter Course objects to those that already took place and that
    should appear on the website.
    """
    def get_query_set(self):
        return super(
            PastCoursePublicManager, self).get_query_set().past().public()


class PastCourse(Course):
    """
    Past courses are Course objects that already took place.

    Past courses that have is_active set to True (=public) appear on
    the past classes section of a branch's website.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Class: Past")

        # Translators: Plural.
        verbose_name_plural = _("Classes: Past")

        ordering = ['-start_time', '-venue']

        proxy = True

    objects = PastCourseManager()
    public = PastCoursePublicManager()


class RejectedCourseManager(CourseManager):
    """
    Filter Course objects to those that have status set to 'pending'.
    """
    def get_query_set(self):
        return super(RejectedCourseManager, self).get_query_set().rejected()


class RejectedCourse(Course):
    """
    Rejected courses are Course objects that have status set to rejeceted.

    Rejected courses are only visible to organizers on the admin backend.
    """
    class Meta:
        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _("Class: Rejected")

        # Translators: Plural.
        verbose_name_plural = _("Classes: Rejected")

        proxy = True

    objects = RejectedCourseManager()


class RegistrationQuerySet(QuerySet):
    """
    Defines querysets for 'truly' registered students.
    """
    def registered(self):
        """
        Returns students that do not only have a relationship
        to a Course, but also who did not unregsiter.
        """
        return self.filter(registration_status='registered')


class RegistrationManager(Manager):
    """
    A Manager selecting related course, barter item titles and student fullname
    """
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
    When a student joins a course, a new Registration object is created.

    It's a Django 'through' model, between Person and Course.

    Registration keeps track of the items the student signed up to bring,
    whether they unregistered.

    Attributes:
        course: Course object that the student registered to.
        student: Person object indicating who registered to a course.
        registration_status: String indicating whether the student
            has unregistered for the course.
        items: M2M relationship of the Course's barter items that the
            student had agreed to bring.
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
                            ('unregistered', _('Unregistered')))

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
        help_text=_("Student registration status")
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
        URL for student to unregister from the Course
        """
        domain = self.course.branch.domain

        return "http://%s%s" % (
            domain, reverse_lazy('course-unregister', kwargs={
                'branch_slug': self.course.branch.slug,
                'course_slug': self.course.slug,
                'student_slug': self.student.slug
            })
        )

    objects = RegistrationManager()

    def registered_item_string(self):
        """
        Create a string with the items the student registered to bring.
        Used in emails sent to students.

        Returns:
            String of line break separated barter item titles
        """
        item_list = ""
        for item in self.items.all():
            item_list += "%s\n" % item.title

        return item_list

    def registered_items(self):
        """
        Formats registered items as a string.
        Used in the admin.

        Returns:
            String of comma separated barter item titles
        """
        return ','.join(str(item) for item in self.items.all())

    def __unicode__(self):
        """
        Returns the student's fullname and their registration status.
        """
        return "%s: %s" % (self.student, self.registration_status)


class Feedback(Base):
    """
    Feedback is collected after courses take place.

    Emails are sent to both students and teacher after a course has taken place
    with a URL to a form where they can leave feedback on a course.

    Feedback is saved anonymously for students. The only indication is whether
    it was received by the teacher or by one of the students.

    Attributes:
        course: Course object that the feedback relates to.
        feedback_type: String indicating whether the feedback was recieved by
            a teacher or a student.
        content: Text of the feedback itself.
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
    An image that appears on the slideshow on a Branch's homepage.

    Attributes:
        filename: Django File object of the image file.
        position: Integar indicating the index of the image in the slideshow.
        branch: Branch object that the image is related to.
    """
    class Meta:
        ordering = ['position', ]

        # Translators: This is used in the header navigation
        # to let you know where you are.
        verbose_name = _('Photo')

        # Translators: Plural
        verbose_name_plural = _('Photos')

    def upload_path(self, filename):
        """
        Save images in a folder assigned to the related branch.

        This folder's name is updated automatically when the title
        of the branch is changed.
        """
        return "uploads/%i/%s" % (self.branch.pk, filename)

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
        """
        Create some HTML that displays a thumbnail of the image.

        Used in the admin.

        Returns:
            HTML string with either an <img> tag or placeholder text
            if there is no image.
        """
        if self.filename:
            return u'<img src="%s" class="branch_image" />' % self.filename.url
        else:
            # Translators: If there are no images
            return _('(No Image)')
        thumbnail.short_description = _('Thumbnail')

    def __unicode__(self):
        return "%s: %s" % (self.branch.title, self.filename)


class PageQuerySet(QuerySet):
    """
    Defines querysets for public and visible branch pages.
    """
    def public(self):
        """
        Returns active pages.
        """
        return self.filter(is_active=True)

    def visible(self):
        """
        Returns pages set to visible.
        """
        return self.filter(is_visible=True)


class PageManager(Manager):
    def get_query_set(self):
        return PageQuerySet(self.model, using=self._db)

    def public(self):
        return self.get_query_set().public()

    def visible(self):
        return self.get_query_set().visible()


class Page(Base):
    """
    Simple model to supply dynamic content pages for each Branch.

    Pages populate the navigation model if they are visible.

    Attributes:
        url: String indicating the unique URL of the Page.
        title: String indicating the Page's header.
        content: HTML text of the body of the page.
        is_visible: Boolean indicating whether the page is visible
            on the navigation menu. Pages that are not visible will
            still be accessible through their URL.
        branch: Foreign key to the Branch that the page is related to.
        position: Integar indicating the index of the image in the slideshow.
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
