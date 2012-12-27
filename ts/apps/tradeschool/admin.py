from tradeschool.models import *
from notifications.models import *
from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    """ Base admin model. Filters objects querysite according to the Site."""
    
    def queryset(self, request):
        """ Filter the queryset using the on site manager 
            in order to only display objects from the current site.
            If the current site is tradeschool.coop (should be SITE_ID = 1),
            display all objects from all sites.        
        """
        qs = super(BaseAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # return everything.
            return qs        
        # use on site manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs   
         
    
class ScheduleInline(admin.TabularInline):
    """ Schedule model inline object. 
        Can be used in the Course Admin view in order 
        to allow on the spot scheduling.
    """
    model   = Schedule
    extra   = 1
    fields  = ('start_time', 'end_time', 'venue')


class RegistrationInline(admin.TabularInline):
    """ Registration model inline object. 
        Used in the Schedule Admin view in order 
        to give an overview of students registered.
    """    
    model   = Registration 
    fields  = ('student', 'registration_status')  
    extra   = 1


class BarterItemInline(admin.TabularInline):
    """ BarterItem model inline object. 
        Used in the Schedule Admin view in order 
        to give an overview of the items requested.
    """    
    model   = BarterItem
    exclude = ('is_active',)    
    extra   = 2


class RegisteredItemInline(admin.TabularInline):
    """ RegisteredItem model inline object. 
        Used in the Registration Admin view in order to 
        give an overview of the items checked by each student.
    """    
    model   = RegisteredItem
    exclude = ('is_active',)    
    extra   = 0


class BranchNotificationInline(admin.TabularInline):
    """ BranchNotification model inline object. 
        Used in the Branch Admin view in order to give 
        an overview of the branch's default email templates.
    """    
    model           = BranchNotification
    fields          = ('email_type', 'subject', 'content',)
    readonly_fields = ('email_type',)
    extra           = 0
    
    
class ScheduleNotificationInline(admin.TabularInline):
    """ ScheduleNotification model inline object. 
        Used in the Schedule Admin view in order to give 
        an overview of the schedule's emails and their status.
    """    
    model   = ScheduleNotification
    extra   = 0
    fields          = ('email_type', 'subject', 'content', 'send_on', 'email_status')
    readonly_fields = ('email_type',)    
    

class BranchAdmin(BaseAdmin):
    """ BranchAdmin lets you add and edit Trade School branches,
        and reset the email templates for each branch.
    """    
    def populate_notifications(self, request, queryset):
        """ call the populate_notifications() method in order to reset email templates for the branch."""
        for branch in queryset:
            branch.populate_notifications()
    populate_notifications.short_description = "Populate Email Notifications"
           
    actions             = ['populate_notifications']            
    list_display        = ('title', 'slug', 'site', 'city', 'country', 'email', 'is_active')
    list_editable       = ('is_active','site',)
    prepopulated_fields = {'slug': ('title',)}
    inlines             = (BranchNotificationInline,)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'site', 'timezone')
        }),
        ('Contact Info', {
            'fields': ('city', 'state', 'country', 'email', 'phone')
        }),
    )


class VenueAdmin(BaseAdmin):
    """ VenueAdmin lets you add and edit venues.
    """    
    list_display    = ('title', 'site', 'address_1', 'city', 'capacity', 'is_active')
    list_editable   = ('site', 'address_1', 'city', 'capacity', 'is_active',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'site',)
        }),
        ('Contact Info', {
            'fields': ('address_1', 'city', 'state', 'country', 'phone')
        }),
        ('Additional Info', {
            'fields': ('capacity', 'resources',)
        }),        
    )       


class CourseAdmin(BaseAdmin):
    """ CourseAdmin lets you add and edit courses
        and their corresponding schedules.
    """    
    list_display         = ('title', 'teacher', 'created')
    search_fields        = ('title', 'teacher__fullname')
    inlines              = (ScheduleInline,)
    fields               = ('title', 'slug', 'teacher', 'max_students', 'category', 'description', 'site')
    prepopulated_fields  = {"slug": ("title",)}
    
    
class PersonAdmin(BaseAdmin):
    """ PersonAdmin lets you add and edit people in the Trade School system,
        and keep track of the classes they took and taught.
    """    
    def queryset(self, request):
        """ Annotate the queryset with counts of registrations and courses taught associated with the Person."""
        return super(PersonAdmin, self).queryset(request).annotate(
            registration_count   = Count('registrations', distinct=True), 
            courses_taught_count = Count('courses_taught', distinct=True)
        )
        
    list_display        = ('fullname', 'email', 'phone', 'courses_taken', 'courses_taught', 'created')    
    search_fields       = ('fullname', 'email', 'phone')
    fields              = ('fullname', 'email', 'phone', 'slug', 'website', 'bio', 'site')
    prepopulated_fields = {'slug': ('fullname',)}

    def courses_taken(self, obj):
        """ Return registration count from annotated queryset so it can be used in list_display."""
        return obj.registration_count
    courses_taken.short_description = 'Courses Taken'
    courses_taken.admin_order_field = 'registration_count'

    def courses_taught(self, obj):
        """ Return courses taught count from annotated queryset so it can be used in list_display."""        
        return obj.courses_taught_count
    courses_taught.short_description = 'Courses Taught'
    courses_taught.admin_order_field = 'courses_taught_count'


class TeacherAdmin(PersonAdmin):
    """ TeacherAdmin lets you add and edit teachers in the Trade School system,
        A Teacher is a proxy model of Person. The only distinction is that a teacher
        is a person who taught at least 1 class.
    """
    def queryset(self, request):
        """ Filter queryset by the courses taught count, so only people who taught at least one class are returned."""
        return super(TeacherAdmin, self).queryset(request).filter(courses_taught_count__gt=0)
            
    list_display = ('fullname', 'email', 'phone', 'courses_taught', 'created')    


class StudentAdmin(PersonAdmin):
    """ StudentAdmin lets you add and edit students in the Trade School system,
        A Student is a proxy model of Person. The only distinction is that a student
        is a person who registered to at least 1 class.
    """    
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(StudentAdmin, self).queryset(request).filter(registration_count__gt=0)


class TimeAdmin(BaseAdmin):
    """ TimeAdmin lets you add and edit time slots in the Trade School system.
    """    
    list_display = ('start_time', 'end_time',)
    fields       = ('start_time', 'end_time', 'site')


class TimeRangeAdmin(BaseAdmin):
    """ TimeRangeAdmin is a way to create batch time slots. A post save signal adds Time objects.
    """    
    list_display = ('start_time', 'end_time', 'start_date', 'end_date',)
    fields       = ('start_time', 'end_time', 'start_date', 'end_date', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'site')


class ScheduleAdmin(BaseAdmin):
    """ ScheduleAdmin lets you add and edit class schedules,
        their barter items, registrations, and email templates.
    """
    def populate_notifications(self, request, queryset):
        """ call the populate_notifications() method in order to reset email templates for the schedule."""        
        for schedule in queryset:
            schedule.populate_notifications()
    populate_notifications.short_description = "Populate Email Notifications"
 
    list_display    = ('course_title', 'teacher_fullname', 'teacher_email', 'start_time', 'end_time', 'venue', 'course_status', 'created', 'updated')
    list_editable   = ('start_time', 'end_time', 'venue', 'course_status', )
    list_filter     = ('course_status', 'venue__title', 'start_time')
    search_fields   = ('get_course_title', 'get_teacher_fullname')
    inlines         = (BarterItemInline, RegistrationInline, ScheduleNotificationInline,)
    actions         = ('approve_courses', 'populate_notifications')
    fieldsets = (
        ('Class Schedule Info', {
            'fields': ('course', 'slug', 'venue', 'course_status')
        }),
        ('Class Time', {
            'fields': ('start_time', 'end_time',)
        }),
    )    

    def course_title(self, obj):
        """ Return related course title so it can be used in list_display."""
        return obj.course.title

    def teacher_fullname(self, obj):
        """ Return related course's teacher so it can be used in list_display."""        
        return obj.course.teacher.fullname
        
    def teacher_email(self, obj):
        """ Return related course's teacher's email so it can be used in list_display."""
        return obj.course.teacher.email


class RegistrationAdmin(BaseAdmin):
    """ RegistrationAdmin lets you add and edit the student registrations
        as well as the items each student signed up to bring.
    """
    fields = ()
    inlines = (RegisteredItemInline,)


class RegisteredItemAdmin(BaseAdmin):
    """ RegisteredItemAdmin is used mostly for introspection. 
        Editing RegisteredItem should be done within the related Registration or Schedule.
    """
    fields = ('barter_item', 'registration', 'registered')


class BarterItemAdmin(BaseAdmin):
    """ BarterItemAdmin is used mostly for introspection. 
        Editing BarterItem should be done within the related Schedule.
    """            
    list_display    = ('title', 'requested',)    
    list_filter     = ('requested',)
    search_fields   = ('title',)
    fields          = ('title', 'requested')
    


# register admin models
admin.site.register(Branch, BranchAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(TimeRange, TimeRangeAdmin)
admin.site.register(BarterItem, BarterItemAdmin)
admin.site.register(RegisteredItem, RegisteredItemAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Feedback)
admin.site.register(Schedule, ScheduleAdmin)