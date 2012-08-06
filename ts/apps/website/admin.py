from website.models import *
from django.contrib import admin

  
class PageAdmin(admin.ModelAdmin):
   list_display = ('branch', 'title', 'is_active')
   list_editable = ('is_active',)
   prepopulated_fields = {'slug': ('title',)}


admin.site.register(Page, PageAdmin)
admin.site.register(Photo)