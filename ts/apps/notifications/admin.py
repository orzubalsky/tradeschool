from tradeschool.admin import BaseAdmin
from notifications.models import *
from admin_enhancer import admin as enhanced_admin
from django.contrib import admin


class StudentConfirmationInline(admin.TabularInline):
    """
    """
    model   = StudentConfirmation
    extra   = 0
    max_num = 1


class StudentReminderInline(admin.TabularInline):
    """
    """
    model   = StudentReminder
    extra   = 0
    max_num = 1


class StudentFeedbackInline(admin.TabularInline):
    """
    """
    model   = StudentFeedback
    extra   = 0
    max_num = 1


class TeacherConfirmationInline(admin.TabularInline):
    """
    """
    model   = TeacherConfirmation
    extra   = 0
    max_num = 1


class TeacherClassApprovalInline(admin.TabularInline):
    """
    """
    model   = TeacherClassApproval
    extra   = 0
    max_num = 1


class TeacherReminderInline(admin.TabularInline):
    """
    """
    model   = TeacherReminder
    extra   = 0
    max_num = 1
                
                
class TeacherFeedbackInline(admin.TabularInline):
    """
    """
    model   = TeacherFeedback
    extra   = 0
    max_num = 1


class BranchEmailContainerAdmin(enhanced_admin.EnhancedModelAdminMixin, admin.ModelAdmin):
    """
    """    
    list_display = ('branch',)
    fields       = ("student_confirmation", "student_reminder", "student_feedback", "teacher_confirmation","teacher_class_approval", "teacher_reminder", "teacher_feedback",)



class ScheduleEmailContainerAdmin(enhanced_admin.EnhancedModelAdminMixin, admin.ModelAdmin):
    """
    """    
    list_display = ('schedule',)
    fields       = ("student_confirmation", "student_reminder", "student_feedback", "teacher_confirmation","teacher_class_approval", "teacher_reminder", "teacher_feedback",)


admin.site.register(DefaultEmailContainer)
admin.site.register(BranchEmailContainer, BranchEmailContainerAdmin)
admin.site.register(ScheduleEmailContainer, ScheduleEmailContainerAdmin)

admin.site.register(StudentConfirmation)
admin.site.register(StudentReminder)
admin.site.register(StudentFeedback)
admin.site.register(TeacherConfirmation)
admin.site.register(TeacherClassApproval)
admin.site.register(TeacherReminder)
admin.site.register(TeacherFeedback)