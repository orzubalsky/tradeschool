from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget, AdminSplitDateTime
from django.conf import settings
from django import forms

class TsAdminTimeWidget(AdminTimeWidget):
    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.MEDIA_URL + "js/admin/DateTimeShortcuts.js")

class TsAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, TsAdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)