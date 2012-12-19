from django.conf import settings
from django.db.models import *
from django_countries import CountryField
from django.contrib.localflavor.us.models import USStateField
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from django.utils.timezone import utc
from datetime import *
import os, sys, pytz, uuid, random
from tradeschool.widgets import *
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class Base(Model):
    """
    Base model for all of the models in ts.  
    """
    class Meta:
            abstract = True
                    
    created     = DateTimeField(auto_now_add=True, editable=False)
    updated     = DateTimeField(auto_now=True, editable=False)
    is_active   = BooleanField(default=1)        
        
    def __unicode__ (self):
        if hasattr(self, "title") and self.title:
            return self.title
        else:
            return "%s #%d" % (type(self), self.id)
            

class Location(Base):
    """
    Abstract for location based models: branch & venue.     
    """
    class Meta:
            abstract = True

    title       = CharField(max_length=100)
    phone       = CharField(max_length=20, blank=True, null=True)    
    city        = CharField(max_length=100)
    state       = USStateField(null=True, blank=True, verbose_name="state")
    country     = CountryField()


class Branch(Location):
    """
    A branch is a ts organization in a specific location (usually city/region).
    The branch slug should be used to point to the individual branch app functionality.
    All dates and times in the branch's view templates should reflect the branch's timezone.   
    """    
    COMMON_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    
    slug        = SlugField(max_length=120, help_text="This is the part that comes after 'http://tradeschool.coop/' in the URL")
    email       = EmailField(max_length=100)
    timezone    = CharField(max_length=100, choices=COMMON_TIMEZONE_CHOICES)
    site        = OneToOneField(Site)

    objects = Manager()
    on_site = CurrentSiteManager()    
    
    def populate_notifications(self):
        "resets branch notification templates from the global branch notification templates"
        
        from notifications.models import BranchNotificationTemplate, BranchNotification
        
        # delete existing branch notifications
        branch_notifications = BranchNotification.objects.filter(branch=self).delete()
        
        # copy branch notification from the branch notification templates
        templates = BranchNotificationTemplate.objects.all()
        for template in templates:
            branch_notification = BranchNotification(branch=self, subject=template.subject, content=template.content, email_type=template.email_type, cron=template.cron)
            branch_notification.save()
    
    # def files(self):
    #         """ the branch's custom files """
    #         return ('base.html', 'subpage.html', 'site.css')
    #         
    #     def folder(self):
    #         """ the folder in which to store the branch's files """        
    #         return settings.BRANCH_FILES + '/%s/' % (self.slug) 
    #         
    #     def create_branch_files(self):
    #         """ create the branch's files in the branch's folder """
    #         for filename in self.files():
    #             filename = self.folder() + filename
    #             if not storage.exists(filename):
    #                 storage.save(filename, ContentFile(''))
    #                     
    #     def delete_branch_files(self):
    #         """ delete files & folder """
    #         for filename in self.files():
    #             filename = self.folder() + filename
    #             if storage.exists(filename):
    #                 storage.delete(filename)
    #         os.rmdir(self.folder())
    #                 
    #     def save (self, *args, **kwargs):
    #         """ save and then create branch files """
    #         super(Branch, self).save(*args, **kwargs)
    #         self.create_branch_files()
    #     
    #     def delete(self):
    #         """ delete and then remove branch files """                        
    #         super(Branch, self).delete()
    #         self.delete_branch_files()


class Venue(Location):
    """
    Each branch has venues in which classes take place.
    *   Normal venues are displayed on the front page calendar.
        Alternative venues are created specifically for classes that require a one-time special location.
        For example, a cooking class has to take place in a kitchen,
        but the kitchen is not open for other classses.
    *   The venue's color is a css hex color that is used in the calendars.
    """

    TYPE_CHOICES = ((0, 'Normal'), (1, 'Alternative'))

    def random_color():
        colorValue = random.randint(0, 16777215)
        return "#%x" % colorValue

    venue_type  = SmallIntegerField(max_length=1, choices=TYPE_CHOICES, default=0)
    address_1   = CharField(max_length=50)
    address_2   = CharField(max_length=100, blank=True, null=True)
    capacity    = SmallIntegerField(max_length=4)     
    resources   = TextField(null=True, default="Chairs, Tables")
    color       = CharField(max_length=7, default=random_color)
    site        = ForeignKey(Site)

    objects = Manager()
    on_site = CurrentSiteManager()    

class PersonManager(Manager):
    pass

class Person(Base):
    """
    Person in the tradeschool system is either a teacher or a student.
    A person submitting a class as a teacher will have to supply a bio as well.
    Hash is used in public urls that involve teachers editing classes & students unregistering
    """
    
    fullname    = CharField(max_length=100, verbose_name="your name", help_text="This will appear on the site.")
    email       = EmailField(max_length=100, verbose_name="Email address", help_text="Used only for us to contact you.")
    phone       = CharField(max_length=20, blank=False, null=True, verbose_name="Cell phone number", help_text="Used only for us to contact you.")
    bio         = TextField(blank=True, verbose_name="A few sentences about you", help_text="For prospective students to see on the website")
    website     = URLField(max_length=200, blank=True, null=True, verbose_name="Your website / blog URL", help_text="Optional.")
    hashcode    = CharField(max_length=32, unique=True, default=uuid.uuid1().hex)
    slug        = SlugField(max_length=120)
    site        = ManyToManyField(Site, null=True)
    
    objects = Manager()
    on_site = CurrentSiteManager()
    
    def __unicode__ (self):
        return self.fullname
    
    def get_courses_taken(self):
        "return the count of courses taken by this person"
        from tradeschool.models import Registration        
        registrations = Registration.objects.filter(student=self)
        return registrations.count()
    get_courses_taken.short_description = 'Classes Taken'
    
    def get_courses_taught(self):
        "return the count of courses taught by this person"
        courses = Course.objects.filter(teacher=self)
        return courses.count()
    get_courses_taught.short_description = 'Classes Taught'    
    
            
class Course(Base):
    """
    The Course class
    """

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    CATEGORIES = (
        (0, 'Arts'),
        (1, 'Etc'),
        (2, 'Food'),
        (3, 'Info'),
        (4, 'Lit'),
        (5, 'Music'),
        (6, 'Org')
    )

    teacher         = ForeignKey(Person)
    category        = SmallIntegerField(max_length=1, choices=CATEGORIES, default=random.randint(0, 6))    
    max_students    = IntegerField(max_length=4, verbose_name="Maximum number of students in your class")
    title           = CharField(max_length=140, verbose_name="class title")    
    slug            = SlugField(max_length=120,blank=False, null=True)
    description     = TextField(blank=False, verbose_name="Class description")
    site       	 	= ManyToManyField(Site, null=True)
    
    objects = Manager()
    on_site = CurrentSiteManager()    

class Durational(Base):
    """
    Durational is an abstract model for any model that has a start time and an end time.
    In the tradeschool system, these would be the Time and Course models.
    """
    class Meta:
		abstract = True

    start_time  = DateTimeField()
    end_time    = DateTimeField()

    formfield_overrides = {
        DateTimeField: {'widget': TsAdminSplitDateTime},
    }
    
    
class Time(Durational):
    """
    Time is an open time slot. It is implemented in the frontend alone:
    These slots populate the calendar for teachers submitting a class.
    Times do not affect the admin class schedluing logic.
    """
    site    = ForeignKey(Site)
    
    objects = Manager()
    on_site = CurrentSiteManager()    


class ScheduleSitePublicManager(Manager):
    def get_query_set(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        return super(ScheduleSitePublicManager, self).get_query_set().filter(course__site__id__exact=settings.SITE_ID).filter(end_time__gte=now).filter(course_status__exact=3).annotate(registered_students=Count('students'))
        
class ScheduleSiteManager(Manager):
    def get_query_set(self):
       return super(ScheduleSiteManager, self).get_query_set().filter(course__site__id__exact=settings.SITE_ID).annotate(registered_students=Count('students')).prefetch_related('course')

class Schedule(Durational):
    """
    """

    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Contacted'),
        (2, 'Updated'),
        (3, 'Approved'),
        (4, 'Rejected')
    )

    venue           = ForeignKey(Venue, null=True, blank=True)
    course          = ForeignKey(Course)
    course_status   = SmallIntegerField(max_length=1, choices=STATUS_CHOICES, default=0)
    hashcode        = CharField(max_length=32, default=uuid.uuid1().hex, unique=True)
    students        = ManyToManyField(Person, through="Registration")    

    objects = Manager()
    on_site = ScheduleSiteManager()    
    public  = ScheduleSitePublicManager()

    def populate_notifications(self):
        "resets course notification templates from the branch notification templates"
        
        from notifications.models import BranchNotification, ScheduleNotification
        
        # delete existing schedule notifications
        schedule_notifications = ScheduleNotification.objects.filter(schedule=self).delete()
        
        # copy course notification from the branch notification templates
        templates = BranchNotification.objects.filter(branch=self.course.teacher.site.branch)
        for template in templates:
            send_on = calculate_send_time()
            schedule_notification = ScheduleNotification(schedule=self, subject=template.subject, content=template.content, email_type=template.email_type, email_status=1, send_on=send_on)
            schedule_notification.save()

    def get_course_title(self):
        "return the title of the associated course"        
        return '%s' % (self.course.title)
    get_course_title.short_description = 'Class'

    def get_teacher_fullname(self):
        "return the full name of the person teaching the associated course"
        return '%s' % (self.course.teacher.fullname)
    get_teacher_fullname.short_description = 'Teacher'

    def approve_courses(self, request, queryset):
        "approve multiple courses"
        rows_updated = queryset.update(course_status=3)
        if rows_updated == 1:
            message_bit = "1 class was"
        else:
            message_bit = "%s classes were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)        
    approve_courses.short_description = "Approve Classes"

    def __unicode__ (self):
        return "%s" % (self.course.title)

class BarterItemSiteManager(Manager):
    def get_query_set(self):
       return super(BarterItemSiteManager, self).get_query_set().filter(schedule__course__site__id__exact=settings.SITE_ID)

class BarterItem(Base):
    """
    Barter items are the items that teachers request for a class they're teaching.
    The items themselves can be requested in various classes, but this model
    keeps track of the items that were requested for a class.
    """

    title       = CharField(max_length=255)
    requested   = IntegerField(max_length=3, default=1)
    schedule    = ForeignKey(Schedule, null=True, blank=False)

    objects = Manager()
    on_site = BarterItemSiteManager()

    def __unicode__ (self):
        return "%s: %i" % (self.title, self.requested)

class RegistrationSiteManager(Manager):
    def get_query_set(self):
       return super(RegistrationSiteManager, self).get_query_set().filter(schedule__course__site__id__exact=settings.SITE_ID)

class Registration(Base):
    """
    Registrations represent connections between students and classes.
    When a student registers to a class a registration row is added.
    We do this because we also want to keep track of students who registered
    and then unregistered from a class.
    """

    REGISTRATION_CHOICES = ((0, 'registered'),(1, 'unregistereed'))

    schedule            = ForeignKey(Schedule)
    student             = ForeignKey(Person)
    registration_status = SmallIntegerField(max_length=1, choices=REGISTRATION_CHOICES, default=0)
    items               = ManyToManyField(BarterItem, through="RegisteredItem")
    
    objects = Manager()
    on_site = RegistrationSiteManager()    

    def __unicode__ (self):      
        return "%s: %s" % (self.student.fullname, self.registration_status)


class RegisteredItemSiteManager(Manager):
    def get_query_set(self):
       return super(RegisteredItemSiteManager, self).get_query_set().filter(registration__schedule__course__teacher__site__id__exact=settings.SITE_ID)

class RegisteredItem(Base):
    """

    """

    registration    = ForeignKey(Registration)
    barter_item     = ForeignKey(BarterItem)
    registered      = IntegerField(max_length=3, default=1)
    
    objects = Manager()
    on_site = RegisteredItemSiteManager()
    
    def __unicode__ (self):
        return "%s: %i" % (self.barter_item.title, self.registered)


class Feedback(Base):
    """
    Feedback is collected after courses take place.
    """

    author      = OneToOneField(Person)
    course      = ForeignKey(Schedule)
    content     = TextField()
    

    def __unicode__ (self):
        return "feedback from %s" % (self.author.fullname)
