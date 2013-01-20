from tradeschool.admin import BaseAdmin
from notifications.models import *
from admin_enhancer import admin as enhanced_admin
from django.contrib import admin


class BranchEmailContainerAdmin(enhanced_admin.EnhancedModelAdminMixin, admin.ModelAdmin):
    """
    """    
    list_display = ('branch',)
    fields       = ("student_confirmation", "student_reminder", "student_feedback", "teacher_confirmation","teacher_class_approval", "teacher_reminder", "teacher_feedback",)



class ScheduleEmailContainerAdmin(enhanced_admin.EnhancedModelAdminMixin, admin.ModelAdmin):
    """
    """    
    list_display  = ('schedule',)
    fields        = ("student_confirmation", "student_reminder", "student_feedback", "teacher_confirmation","teacher_class_approval", "teacher_reminder", "teacher_feedback",)


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