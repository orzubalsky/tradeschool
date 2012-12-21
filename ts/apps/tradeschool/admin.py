from tradeschool.models import *
from notifications.models import *
from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(BaseAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs    
    
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ('venue', 'start_time', 'end_time')

class RegistrationInline(admin.TabularInline):
    model = Registration 
    fields = ('student', 'registration_status')  
    extra = 0       

class BarterItemInline(admin.TabularInline):
    model = BarterItem
    exclude = ('is_active',)    
    extra = 0

class RegisteredItemInline(admin.TabularInline):
    model = RegisteredItem
    exclude = ('is_active',)    
    extra = 0

class BranchNotificationInline(admin.TabularInline):
    model = BranchNotification
    extra = 0
    
class ScheduleNotificationInline(admin.TabularInline):
    model = ScheduleNotification
    extra = 0    

class BranchAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(BranchAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def populate_notifications(self, request, queryset):
        for branch in queryset:
            branch.populate_notifications()
    populate_notifications.short_description = "Populate Email Notifications"
           
    actions = ['populate_notifications']            
    list_display = ('title', 'slug','site','city','country', 'email', 'is_active')
    list_editable = ('is_active','site',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'site', 'timezone')
        }),
        ('Contact Info', {
            'fields': ('city', 'state', 'country', 'email', 'phone')
        }),
    )
    inlines = (BranchNotificationInline,)
       
       
class VenueAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(VenueAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
            
    list_display = ('title', 'site', 'is_active')
    list_editable = ('is_active','site',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'site',)
        }),
        ('Contact Info', {
            'fields': ('city', 'state', 'country', 'phone')
        }),
    )       

class CourseAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(CourseAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
            
    list_display = ('title', 'teacher', 'created')    
    search_fields = ('title', 'teacher__fullname')
    fields = (('title', 'slug'), ('teacher', 'max_students', 'category'), 'description')
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ScheduleInline,)
    
class PersonAdmin(BaseAdmin):
    def queryset(self, request):
        return super(PersonAdmin, self).queryset(request).annotate(
            registration_count  =Count('registrations', distinct=True), 
            courses_taught_count=Count('courses_taught', distinct=True)
        )
        
    list_display = ('fullname', 'email', 'phone', 'courses_taken', 'courses_taught', 'created')    
    search_fields = ('fullname', 'email', 'phone')
    fields = (('fullname', 'email', 'phone', 'slug'), 'website', 'bio')
    prepopulated_fields = {'slug': ('fullname',)}

    def courses_taken(self, obj):
        return obj.registration_count
    courses_taken.short_description = 'Courses Taken'
    courses_taken.admin_order_field = 'registration_count'

    def courses_taught(self, obj):
        return obj.courses_taught_count
    courses_taught.short_description = 'Courses Taught'
    courses_taught.admin_order_field = 'courses_taught_count'


class TeacherAdmin(PersonAdmin):
    def queryset(self, request):
        return super(TeacherAdmin, self).queryset(request).filter(courses_taught_count__gt=0)
            
    list_display = ('fullname', 'email', 'phone', 'courses_taught', 'created')    


class StudentAdmin(PersonAdmin):
    def queryset(self, request):
        return super(StudentAdmin, self).queryset(request).filter(registration_count__gt=0)


class TimeAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(TimeAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
            
    formfield_overrides = {
            DateTimeField: {'widget': TsAdminSplitDateTime},
        }    
    list_display = ('start_time', 'end_time',)

class ScheduleAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ScheduleAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
                    
    def populate_notifications(self, request, queryset):
        for schedule in queryset:
            schedule.populate_notifications()
    populate_notifications.short_description = "Populate Email Notifications"

    list_display = ('get_course_title', 'get_teacher_fullname', 'start_time', 'end_time', 'venue', 'course_status', 'created')    
    list_editable = ('course_status', )
    list_filter = ('course_status', 'venue__title', 'start_time')
    search_fields = ('get_course_title', 'get_teacher_fullname')
    fields = (('course', 'venue', 'course_status'), ('start_time', 'end_time'))
    inlines = (RegistrationInline, BarterItemInline, ScheduleNotificationInline,)
    actions = ('approve_courses', 'populate_notifications')

class RegistrationAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(RegistrationAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
            
    fields = ()
    inlines = (RegisteredItemInline,)

class RegisteredItemAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(RegisteredItemAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    fields = ()

class BarterItemAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(BarterItemAdmin, self).queryset(request)        
        if settings.SITE_ID == 1:
            # It is mine, all mine. Just return everything.
            return qs        
        # use our manager, rather than the default one
        qs = self.model.on_site.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
            
    list_display = ('title', 'requested',)    
    list_filter = ('requested',)
    search_fields = ('title',)
    fields = (('title', 'requested'),)
    


admin.site.register(Branch, BranchAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(BarterItem, BarterItemAdmin)
admin.site.register(RegisteredItem, RegisteredItemAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Feedback)
admin.site.register(Schedule, ScheduleAdmin)
