from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.admin import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from flatpages_tinymce.admin import FlatPageAdmin
from django.contrib import admin
from admin_enhancer import admin as enhanced_admin
from tradeschool.models import *
from tradeschool.forms import *


class BaseAdmin(enhanced_admin.EnhancedModelAdminMixin, admin.ModelAdmin):
    """Base admin model. Filters objects querysite according to the current branch."""

    def queryset(self, request, q=None):
        """
        queryset is filtered against the Branch objects that the logged in Person is organizing.
        In the case the logged in Person is a superuser, they see all of the data without filtering.
        """
        qs = super(BaseAdmin, self).queryset(request)

        if not request.user.is_superuser:
            # other users see data filtered by the branch they're associated with
            if q == None:
                q = Q(branches__in=request.user.branches_organized.all)
            qs = qs.filter(q)

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)

        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'branch':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Branch, Q(pk__in=request.user.branches_organized.all))
        return super(BaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'branches':
            qs = Branch.objects.filter(pk__in=request.user.branches_organized.all)            
            kwargs['queryset'] = qs
            kwargs['initial'] = [qs[0],]
        return super(BaseAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
    def filter_dbfield(self, request, model, q, **kwargs):
        qs = model.objects.filter(q)
        kwargs['queryset'] = qs
        if qs.count() > 0:
            kwargs['initial'] = qs[0]
        return kwargs['queryset'], kwargs['initial']
  

class BaseTabularInline(admin.TabularInline):
    def queryset(self, request, q):
        """
        queryset is filtered against the Branch objects that the logged in Person is organizing.
        In the case the logged in Person is a superuser, they see all of the data without filtering.
        """
        qs = super(BaseTabularInline, self).queryset(request)

        if not request.user.is_superuser:
            # other users see data filtered by the branch they're associated with
            qs = qs.filter(q)

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)

        if ordering:
            qs = qs.order_by(*ordering)
        return qs    

    def filter_dbfield(self, request, model, q, **kwargs):
        qs = model.objects.filter(q)
        kwargs['queryset'] = qs
        if qs.count() > 0:
            kwargs['initial'] = qs[0]
        return kwargs['queryset'], kwargs['initial']


class BaseStackedInline(admin.StackedInline):
    def queryset(self, request, q):
        """
        queryset is filtered against the Branch objects that the logged in Person is organizing.
        In the case the logged in Person is a superuser, they see all of the data without filtering.
        """
        qs = super(BaseStackedInline, self).queryset(request)

        if not request.user.is_superuser:
            # other users see data filtered by the branch they're associated with
            qs = qs.filter(q)

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)

        if ordering:
            qs = qs.order_by(*ordering)
        return qs
                

class TimedEmailBranchInline(BaseTabularInline):
    """TimedEmailBranchInline"""
    def queryset(self, request):
        return super(TimedEmailBranchInline, self).queryset(request, Q())        
    extra   = 0
    max_num = 0    
    fields  = ('subject', 'content', 'days_delta', 'send_time')


class TimedEmailScheduleInline(BaseTabularInline):
    """TimedEmailScheduleInline"""
    def queryset(self, request):
        return super(TimedEmailScheduleInline, self).queryset(request, Q())        
    extra   = 0
    max_num = 0    
    fields  = ('subject', 'content', 'email_status', 'send_on')


class EmailBranchInline(BaseTabularInline):
    """
    """
    def queryset(self, request):
        return super(EmailBranchInline, self).queryset(request, Q())
    extra   = 0
    max_num = 0
    fields  = ('subject', 'content')
        

class EmailScheduleInline(BaseTabularInline):
    """
    """
    def queryset(self, request):
        return super(EmailScheduleInline, self).queryset(request, Q())
    extra   = 0
    max_num = 0
    fields  = ('subject', 'content', 'email_status')


class StudentConfirmationBranchInline(EmailBranchInline):
    model   = StudentConfirmation


class StudentConfirmationScheduleInline(EmailScheduleInline):
    model   = StudentConfirmation


class StudentReminderBranchInline(TimedEmailBranchInline):
    model   = StudentReminder


class StudentReminderScheduleInline(TimedEmailScheduleInline):
    model   = StudentReminder


class StudentFeedbackBranchInline(TimedEmailBranchInline):
    model   = StudentFeedback


class StudentFeedbackScheduleInline(TimedEmailScheduleInline):
    model   = StudentFeedback


class TeacherConfirmationBranchInline(EmailBranchInline):
    model   = TeacherConfirmation


class TeacherConfirmationScheduleInline(EmailScheduleInline):
    model   = TeacherConfirmation


class TeacherClassApprovalBranchInline(EmailBranchInline):
    model   = TeacherClassApproval


class TeacherClassApprovalScheduleInline(EmailScheduleInline):
    model   = TeacherClassApproval


class TeacherReminderBranchInline(TimedEmailBranchInline):
    model   = TeacherReminder


class TeacherReminderScheduleInline(TimedEmailScheduleInline):
    model   = TeacherReminder


class TeacherFeedbackBranchInline(TimedEmailBranchInline):
    model   = TeacherFeedback


class TeacherFeedbackScheduleInline(TimedEmailScheduleInline):
    model   = TeacherFeedback


class OrganizedBranchInline(BaseTabularInline):
    """
    """    
    def queryset(self, request):
        return super(OrganizedBranchInline, self).queryset(request, Q())        

    model = Branch.organizers.through
    extra = 1


class ClusteredBranchInline(BaseTabularInline):
    """
    """    
    def queryset(self, request):
        return super(ClusteredBranchInline, self).queryset(request, Q())        

    model = Branch.clusters.through
    extra = 1


class ScheduleInline(BaseTabularInline):
    """Schedule model inline object. 
        Can be used in the Course Admin view in order 
        to allow on the spot scheduling."""
    
    def queryset(self, request):
        return super(ScheduleInline, self).queryset(request, Q(course__branches__in=request.user.branches_organized.all))        
                
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'venue':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Venue, Q(branch__in=request.user.branches_organized.all))
        return super(ScheduleInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    model   = Schedule
    extra   = 0
    fields  = ('start_time', 'end_time', 'venue')


class RegistrationInline(enhanced_admin.EnhancedModelAdminMixin, BaseTabularInline):
    """Registration model inline object. 
        Used in the Schedule Admin view in order 
        to give an overview of students registered."""

    def queryset(self, request):
        return super(RegistrationInline, self).queryset(request, Q(schedule__course__branches__in=request.user.branches_organized.all))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Student, Q(branch__in=request.user.branches_organized.all))
        return super(RegistrationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def registration_link(self, obj):
        """
        """
        # link to item edit admin form 
        url = reverse('admin:tradeschool_registration_change', args=(obj.pk,))
        html = '<a target="_blank" href="%s">%s</a>' % (url, obj.student.fullname)
        return mark_safe(html)
    
    registration_link.short_description = _('Title')
        
    model           = Registration 
    readonly_fields = ('registration_link', 'items', 'registration_status')
    fields          = ('registration_link', 'items', 'registration_status',)
    extra           = 0


class BarterItemInline(BaseTabularInline):
    """BarterItem model inline object. 
        Used in the Schedule Admin view in order 
        to give an overview of the items requested."""

    def queryset(self, request):
        return super(BarterItemInline, self).queryset(request, Q(schedule__course__branches__in=request.user.branches_organized.all))        
    
    def title_link(self, obj):
        """
        """
        # link to item edit admin form 
        url = reverse('admin:tradeschool_barteritem_change', args=(obj.pk,))
        html = '<a target="_blank" href="%s">%s</a>' % (url, obj.title)
        return mark_safe(html)
    
    title_link.short_description = _('Title')
         
    model           = BarterItem
    fields          = ('title_link',)
    readonly_fields = ('title_link',)
    extra           = 0


class PhotoInline(enhanced_admin.EnhancedAdminMixin, BaseTabularInline):
    """
    """

    def queryset(self, request):
        return super(PhotoInline, self).queryset(request, Q(branch__in=request.user.branches_organized.all))
            
    model               = Photo
    fields              = ('render_image', 'filename', 'position',)
    readonly_fields     = ('render_image',)
    extra               = 0
    sortable_field_name = "position"
    
    def render_image(self, obj):
        return mark_safe("""<img src="%s" class="branch_image"/>""" % obj.filename.url)    
    render_image.short_description = _("Thumbnail")


class FeedbackInline(enhanced_admin.EnhancedAdminMixin, BaseTabularInline):
    """
    """
    def queryset(self, request):
        return super(FeedbackInline, self).queryset(request, Q(schedule__course__branches__in=request.user.branches_organized.all))
    
    model   = Feedback
    fields = ('feedback_type', 'content',)
    readonly_fields = ('feedback_type',)
    extra   = 0


class BranchAdmin(BaseAdmin):
    """BranchAdmin lets you add and edit tradeschool branches,
        and reset the email templates for each branch.
        """
    def queryset(self, request):
        return super(BranchAdmin, self).queryset(request, Q(pk__in=request.user.branches_organized.all))
           
    form = BranchForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = ( 
                        StudentConfirmationBranchInline,
                        TeacherConfirmationBranchInline,
                        TeacherClassApprovalBranchInline,
                        TeacherReminderBranchInline,
                        TeacherFeedbackBranchInline,
                        StudentReminderBranchInline,
                        StudentFeedbackBranchInline,                            
                        PhotoInline,
                    )       
        return super(BranchAdmin, self).change_view(request, object_id)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (PhotoInline, )
        return super(BranchAdmin, self).add_view(request)

    def populate_notifications(self, request, queryset):
        """call the populate_notifications() method in order to reset email templates for the branch."""
        
        for branch in queryset:
            branch.populate_notifications()
    populate_notifications.short_description = _("Generate Email Notifications")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'organizers':
            qs = Person.objects.filter(is_staff=True)            
            kwargs['queryset'] = qs
        return super(BranchAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    list_display        = ('title', 'slug', 'site', 'city', 'country', 'email', 'branch_status', 'is_active')
    list_editable       = ('is_active', 'branch_status',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ('organizers', 'clusters')
    inlines             = ()       
    fieldsets = (
        # Translators: This is the a header in the branch admin form
        (_('Basic Info'), {
            'fields': ('title', 'slug', 'timezone', 'language', 'branch_status')
        }),
        # Translators: This is the a header in the branch admin form
        (_('Contact Info'), {
            'fields': ('city', 'state', 'country', 'email', 'phone')
        }),
        # Translators: This is the a header in the branch admin form
        (_('Website Content'), {
            'fields': ('header_copy', 'intro_copy', 'footer_copy')
        }), 
        # Translators: This is the a header in the branch admin form       
        (_('Organizers'), {
            'fields': ('organizers', 'clusters')
        }),        
    )


class VenueAdmin(BaseAdmin):
    """VenueAdmin lets you add and edit venues."""

    def queryset(self, request):
        return super(VenueAdmin, self).queryset(request, Q(branch__in=request.user.branches_organized.all))
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'country':
            kwargs['initial'] = Branch.objects.filter(pk__in=request.user.branches_organized.all)[0].country
        if db_field.name == 'state':
            kwargs['initial'] = Branch.objects.filter(pk__in=request.user.branches_organized.all)[0].state
        return super(VenueAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
                
    list_display    = ('title', 'branch', 'address_1', 'city', 'capacity', 'is_active')
    list_editable   = ('address_1', 'city', 'capacity', 'is_active',)
    fieldsets = (
        # Translators: This is the a header in the branch admin form
        (_('Basic Info'), {
            'fields': ('title', 'branch',)
        }),
        # Translators: This is the a header in the branch admin form
        (_('Contact Info'), {
            'fields': ('address_1', 'city', 'state', 'country', 'phone')
        }),
        # Translators: This is the a header in the branch admin form
        (_('Additional Info'), {
            'fields': ('capacity', 'resources',)
        }),        
    )       


class CourseAdmin(BaseAdmin):
    """CourseAdmin lets you add and edit courses
        and their corresponding schedules."""

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Teacher, Q(branches__in=request.user.branches_organized.all))
        return super(CourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
 
    list_display         = ('title', 'teacher', 'created')
    search_fields        = ('title', 'teacher__fullname')
    inlines              = (ScheduleInline,)
    fields               = ('title', 'slug', 'teacher', 'max_students', 'category', 'description')
    prepopulated_fields  = {'slug': ('title',)}
    
    
class PersonAdmin(BaseAdmin):
    """ PersonAdmin lets you add and edit people in the Trade School system,
        and keep track of the classes they took and taught.
    """ 

    def queryset(self, request, q=None):
        """ Annotate the queryset with counts of registrations and courses taught associated with the Person."""
        return super(PersonAdmin, self).queryset(request).annotate(
            registration_count   = Count('registrations', distinct=True), 
            courses_taught_count = Count('courses_taught', distinct=True)
        )
            
    list_display        = ('fullname', 'email', 'phone', 'courses_taken', 'courses_taught', 'branches_string', 'created')
    search_fields       = ('fullname', 'email', 'phone')
    fields              = ('fullname', 'username', 'email', 'phone', 'website', 'bio')
    #prepopulated_fields = {'slug': ('username',)}

    def courses_taken(self, obj):
        """ Return registration count from annotated queryset so it can be used in list_display."""
        return obj.registration_count
    courses_taken.short_description = 'Courses Taken'
    courses_taken.admin_order_field = 'registration_count'

    def courses_taught(self, obj):
        """ Return courses taught count from annotated queryset so it can be used in list_display."""        
        return obj.courses_taught_count
    courses_taught.short_description = _('Courses Taught')
    courses_taught.admin_order_field = 'courses_taught_count'


class OrganizerAdmin(PersonAdmin):
    """
    """
    def change_password_link(self, obj):
        """
        """
        # link to change password admin form 
        url = reverse('admin:password_change', args=(obj.course.pk,))
        html = '<a target="_blank" href="%s">change password</a>' % (url,)
        return mark_safe(html)
    change_password_link.short_description = _('change password')
            
    list_display = ('username', 'fullname', 'email', 'branches_organized_string')
    fields       = ('username', 'fullname', 'email', 'language',)
    inlines      = (OrganizedBranchInline,)


class TeacherAdmin(PersonAdmin):
    """ TeacherAdmin lets you add and edit teachers in the Trade School system,
        A Teacher is a proxy model of Person. The only distinction is that a teacher
        is a person who taught at least 1 class.
    """
    def queryset(self, request):
        """ Filter queryset by the courses taught count, so only people who taught at least one class are returned."""
        return super(TeacherAdmin, self).queryset(request, Q(courses_taught_count__gt=0, branches__in=request.user.branches_organized.all))

    list_display = ('fullname', 'email', 'phone', 'courses_taught', 'created')    


class StudentAdmin(PersonAdmin):
    """ StudentAdmin lets you add and edit students in the Trade School system,
        A Student is a proxy model of Person. The only distinction is that a student
        is a person who registered to at least 1 class.
    """    
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(StudentAdmin, self).queryset(request, Q(registration_count__gt=0, branches__in=request.user.branches_organized.all))


class TimeAdmin(BaseAdmin):
    """ TimeAdmin lets you add and edit time slots in the Trade School system.
    """    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TimeAdmin, self).get_form(request, obj, **kwargs)
        
        if obj is not None:
            form.base_fields['venue'].queryset = Venue.objects.filter(branch=obj.branch)
            form.base_fields['branch'].queryset = Branch.objects.filter(pk=obj.branch.pk)
        else:
            form.base_fields['venue'].queryset = Venue.objects.filter(branch__in=request.user.branches_organized.all)
            form.base_fields['branch'].queryset = Branch.objects.filter(pk__in=request.user.branches_organized.all)            
            form.base_fields['branch'].initial = request.user.branches_organized.all()[0]
            
        return form

    def queryset(self, request):
        return super(TimeAdmin, self).queryset(request, Q(branch__in=request.user.branches_organized.all))
            
    list_display  = ('start_time', 'end_time', 'venue')
    fields        = ('start_time', 'end_time', 'venue', 'branch')


class TimeRangeAdmin(BaseAdmin):
    """ TimeRangeAdmin is a way to create batch time slots. A post save signal adds Time objects.
    """    
    def queryset(self, request):
        return super(TimeRangeAdmin, self).queryset(request, Q(branch__in=request.user.branches_organized.all))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):  
        if db_field.name == 'venue':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Venue, Q(is_active=True, branch__in=request.user.branches_organized.all))
        if db_field.name == 'branch':          
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Branch, Q(pk__in=request.user.branches_organized.all))
            kwargs['queryset'] = Branch.objects.filter(pk__in=request.user.branches_organized.all)

        return super(TimeRangeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
             
    list_display = ('start_time', 'end_time', 'start_date', 'end_date', 'venue')
    fields       = ('start_time', 'end_time', 'start_date', 'end_date', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'venue', 'branch')


class ScheduleAdmin(BaseAdmin):
    """ ScheduleAdmin lets you add and edit class schedules,
        their barter items, registrations, and email templates.
    """ 
    def queryset(self, request):
        return super(ScheduleAdmin, self).queryset(request, Q(course__branches__in=request.user.branches_organized.all))

    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs['request']
        formfield = super(ScheduleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'venue':
            venue_choices_cache = getattr(request, 'venue_choices_cache', None)
            if venue_choices_cache is not None:
                formfield.choices = venue_choices_cache
            else:
                request.venue_choices_cache = formfield.choices
        return formfield

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'venue':
            pass
            #kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Venue, Q(branch__in=request.user.branches_organized.all))
        if db_field.name == 'course':
            pass
            #kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Course, Q(branches__in=request.user.branches_organized.all))
        return super(ScheduleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = ( 
                        BarterItemInline, 
                        RegistrationInline,
                        StudentConfirmationScheduleInline,
                        TeacherConfirmationScheduleInline,
                        TeacherClassApprovalScheduleInline,
                        TeacherReminderScheduleInline,
                        TeacherFeedbackScheduleInline,
                        StudentReminderScheduleInline,
                        StudentFeedbackScheduleInline,                           
                        FeedbackInline,
                    )       
        return super(ScheduleAdmin, self).change_view(request, object_id)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (BarterItemInline, )
        return super(ScheduleAdmin, self).add_view(request)

    def populate_notifications(self, request, queryset):
        """ call the populate_notifications() method in order to reset email templates for the schedule."""        
        for schedule in queryset:
            schedule.populate_notifications()
    populate_notifications.short_description = _("Generate Email Notifications")

    def course_title(self, obj):
        """ Return related course title so it can be used in list_display."""
        return obj.course.title
    course_title.short_description = _('Courses Title')
    
    def course_title_link(self, obj):
        """ Return related course title so it can be used in list_display."""
        # link to course edit admin form 
        url = reverse('admin:tradeschool_course_change', args=(obj.course.pk,))
        html = '<a target="_blank" href="%s">%s</a>' % (url, obj.course.title)
        return mark_safe(html)
    course_title_link.short_description = _('Course title link')

    def course_description(self, obj):
        """ Return related course's description so it can be used in list_display."""
        return obj.course.description
    course_description.short_description = _('Course description')

    def course_max_students(self, obj):
        """ Return related course's max students so it can be used in list_display."""
        return obj.course.max_students
    course_max_students.short_description = _('Course Max Students')
            
    def teacher_fullname(self, obj):
        """ Return related course's teacher so it can be used in list_display."""        
        teacher = obj.course.teacher
        # link to teacher edit admin form 
        url = reverse('admin:tradeschool_teacher_change', args=(teacher.pk,))
        html = '<a target="_blank" href="%s">%s</a>' % (url, teacher.fullname)
        return mark_safe(html)
    teacher_fullname.short_description = _('Teacher Fullname')
        
    def teacher_email(self, obj):
        """ Return related course's teacher's email so it can be used in list_display."""
        html = '<a href="mailto:%s">%s</a>' % (obj.course.teacher.email, obj.course.teacher.email)
        return mark_safe(html)
    teacher_email.short_description = _('Teacher Email')
    
    def teacher_phone(self, obj):
        """ Return related course's teacher's phone so it can be used in list_display."""
        return obj.course.teacher.phone
    teacher_phone.short_description = _('Teacher phone')
    
    def teacher_bio(self, obj):
        """ Return related course's teacher's bio so it can be used in list_display."""
        return obj.course.teacher.bio
    teacher_bio.short_description = _('Teacher bio')
    
    def teacher_website(self, obj):
        """ Return related course's teacher's website so it can be used in list_display."""
        return obj.course.teacher.website
    teacher_website.short_description = _('Teacher website')
    
    def get_form(self, request, obj=None, **kwargs):
        # Proper kwargs are form, fields, exclude, formfield_callback
        if obj: # obj is not None, so this is a change page
            fieldsets = (
                # Translators: This is the a header in the branch admin form
                (_('Class Info'), {
                    'fields': ('course_title_link', 'course_description', 'course_max_students', 'slug')
                }),
                # Translators: This is the a header in the branch admin form
                (_('Teacher Info'), {
                    'fields': ('teacher_fullname', 'teacher_email', 'teacher_phone', 'teacher_bio', 'teacher_website')
                }), 
                # Translators: This is the a header in the branch admin form       
                (_('Class Schedule'), {
                    'fields': ('venue', 'start_time', 'end_time', 'schedule_status')
                }),     
            )
            kwargs['fields'] = ()
        else: # obj is None, so this is an add page
            pass

        return super(ScheduleAdmin, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + (
                        'course_description',
                        'course_max_students',
                        'teacher_fullname', 
                        'teacher_email', 
                        'teacher_bio', 
                        'teacher_website', 
                        'teacher_phone',
                    )
        return self.readonly_fields

    list_display    = (
                        'course_title', 
                        'teacher_fullname', 
                        'teacher_email', 
                        'start_time', 
                        'end_time', 
                        'venue', 
                        'schedule_status', 
                        'created'
                        )
    list_editable   = (
                        'start_time', 
                        'end_time', 
                        'venue', 
                        'schedule_status',
                        )
    list_filter     = (
                        'schedule_status', 
                        'venue', 
                        'start_time'
                        )
    readonly_fields = ()
    search_fields   = (
                        'get_course_title', 
                        'get_teacher_fullname'
                        )
    inlines         = ()
    actions         = (
                        'approve_courses', 
                        'populate_notifications'
                        )

    #prepopulated_fields  = {'slug': ('start_time',) }


class PendingScheduleAdmin(ScheduleAdmin):
    """
    """
    def response_change(self, request, obj):
        """
        If the schedule_status was changed to 'approved', redirect to the ApprovedSchedule change-view
        """
        response = super(PendingScheduleAdmin, self).response_change(request, obj)

        # only redirect if the schedule was saved by clicking on "save and continue editing"
        if (isinstance(response, HttpResponseRedirect) and request.POST.has_key('_continue')):
            
            if obj.schedule_status == 'approved':
                url = reverse('admin:tradeschool_approvedschedule_change', args=(obj.pk,))

                response['location'] = url

        return response


class ApprovedScheduleAdmin(ScheduleAdmin):
    def response_change(self, request, obj):
        """
        If the schedule_status was changed from 'approved', redirect to the PendingSchedule change-view
        """
        response = super(ApprovedScheduleAdmin, self).response_change(request, obj)

        # only redirect if the schedule was saved by clicking on "save and continue editing"
        if (isinstance(response, HttpResponseRedirect) and request.POST.has_key('_continue')):
            
            if obj.schedule_status is not 'approved':
                url = reverse('admin:tradeschool_pendingschedule_change', args=(obj.pk,))

                response['location'] = url

        return response


class PastScheduleAdmin(ScheduleAdmin):
    pass


class RegistrationAdmin(BaseAdmin):
    """ RegistrationAdmin lets you add and edit the student registrations
        as well as the items each student signed up to bring.
    """
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(RegistrationAdmin, self).queryset(request, Q(schedule__course__branches__in=request.user.branches_organized.all))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Student, Q(branches__in=request.user.branches_organized.all))
        if db_field.name == 'schedule':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Schedule, Q(course__branches__in=request.user.branches_organized.all))
        return super(RegistrationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'items':
            # parsing the object id from the URL. **This is very ugly! is there a way to get the obj from the request --Or
            try:
                registration_pk = int(request.path.split('/')[4])
                registration = Registration.objects.get(pk=registration_pk)
                kwargs['queryset'] = BarterItem.objects.filter(schedule=registration.schedule)
            except ValueError:
                pass
        return super(RegistrationAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)        
            
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + (
                        'student', 
                        'schedule'
                    )
        return self.readonly_fields

    fields              = ('student', 'schedule', 'items', 'registration_status')
    readonly_fields     = ()
    list_display        = ('student', 'schedule', 'registered_items', 'registration_status', 'branches_string')
    filter_horizontal   = ('items',)


class BarterItemAdmin(BaseAdmin):
    """ BarterItemAdmin is used mostly for introspection. 
        Editing BarterItem should be done within the related Schedule.
    """
    
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(BarterItemAdmin, self).queryset(request, Q(registration__schedule__course__branches__in=request.user.branches_organized.all))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'schedule':
            kwargs['queryset'], kwargs['initial'] = self.filter_dbfield(request, Schedule, Q(course__branches__in=request.user.branches_organized.all, schedule_status='approved'))
        return super(BarterItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            
    list_display    = ('title', 'schedule')    
    search_fields   = ('title', 'schedule')
    fields          = ('title', 'schedule')



class PhotoAdmin(BaseAdmin):
    """ 
    """    
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(PhotoAdmin, self).queryset(request, Q(branch__in=request.user.branches_organized.all))

    list_display    = ('get_thumbnail', 'filename', 'position', 'branch')
    
    def get_thumbnail(self, obj):
        """ """
        return obj.thumbnail() 
    get_thumbnail.short_description = _('Thumbnail')
    get_thumbnail.allow_tags = True        


class BranchEmailContainerAdmin(BaseAdmin, enhanced_admin.EnhancedModelAdminMixin):
    """
    """
    def queryset(self, request):
        return super(BranchEmailContainerAdmin, self).queryset(request, Q(branch__in=request.user.branches_organized.all))

    list_display = ('branch',)
    fields       = ("student_confirmation", "student_reminder", "student_feedback", "teacher_confirmation","teacher_class_approval", "teacher_reminder", "teacher_feedback",)


class ScheduleEmailContainerAdmin(BaseAdmin, enhanced_admin.EnhancedModelAdminMixin):
    """
    """
    def queryset(self, request):
        return super(ScheduleEmailContainerAdmin, self).queryset(request, Q(schedule__course__branches__in=request.user.branches_organized.all))
    
    list_display  = ('schedule', 'branches_string')
    fields        = ("student_confirmation", "student_reminder", "student_feedback", "teacher_confirmation","teacher_class_approval", "teacher_reminder", "teacher_feedback",)


class BranchPageForm(FlatpageForm):
    class Meta:
        model = BranchPage
  

class BranchPageAdmin(BaseAdmin, FlatPageAdmin):
    """ """
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(BranchPageAdmin, self).queryset(request, Q(branch__in=request.user.branches_organized.all))
            
    form = BranchPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'branch')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'is_visible', 'template_name')}),
    )
    list_display = ('title', 'url', 'branch', 'is_visible')
    list_filter = ('sites', 'branch', 'enable_comments', 'registration_required')
    list_editable = ('is_visible',)
    search_fields = ('url', 'title') 
    

class FeedbackAdmin(BaseAdmin, enhanced_admin.EnhancedModelAdminMixin):
    """
    """
    def queryset(self, request):
        """ Filter queryset by the registration count, so only people who took at least one class are returned."""        
        return super(FeedbackAdmin, self).queryset(request, Q(schedule__course__branches__in=request.user.branches_organized.all))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'schedule':
            kwargs['queryset'] = Schedule.objects.filter(course__branches__in=request.user.branches_organized.all)
        return super(FeedbackAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    list_display = ('schedule', 'feedback_type')
    fields       = ('schedule', 'feedback_type', 'content',)
    

class ClusterAdmin(BaseAdmin, enhanced_admin.EnhancedModelAdminMixin):
    """
    """
    def queryset(self, request):
        return super(ClusterAdmin, self).queryset(request, Q())
        
    list_display = ('name', 'slug', 'branches_string')
    fields       = ('name', 'slug',)
    inlines      = (ClusteredBranchInline,)



# register admin models
admin.site.register(Branch, BranchAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Cluster, ClusterAdmin)

admin.site.register(PendingSchedule, PendingScheduleAdmin)
admin.site.register(ApprovedSchedule, ApprovedScheduleAdmin)
admin.site.register(PastSchedule, PastScheduleAdmin)

admin.site.register(BarterItem, BarterItemAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Feedback, FeedbackAdmin)

admin.site.register(Person, PersonAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)

admin.site.register(Time, TimeAdmin)
admin.site.register(TimeRange, TimeRangeAdmin)

admin.site.unregister(FlatPage)
admin.site.register(BranchPage, BranchPageAdmin)
admin.site.register(Photo, PhotoAdmin)

admin.site.register(DefaultEmailContainer)

admin.site.register(StudentConfirmation)
admin.site.register(StudentReminder)
admin.site.register(StudentFeedback)
admin.site.register(TeacherConfirmation)
admin.site.register(TeacherClassApproval)
admin.site.register(TeacherReminder)
admin.site.register(TeacherFeedback)