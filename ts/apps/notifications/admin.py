from notifications.models import *
from django.contrib import admin

admin.site.register(BranchNotificationTemplate)
admin.site.register(BranchNotification)
admin.site.register(ScheduleNotification)