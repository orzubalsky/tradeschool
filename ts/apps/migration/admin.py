# -*- coding: utf-8 -*-
from migration.models import *
from django.contrib import admin
from django.template.defaultfilters import slugify
      
def migrate(modeladmin, request, queryset): 
    "create an intance of the tradeschool app model"  
    
    # iterate over selected rows
    for old_db_model in queryset:
        # get fields and values for each db row
        data = {k: v for k,v in old_db_model.__dict__.items()}

        # call the appropriate function, according to the rules dictionary
        modeladmin.model.objects.migrate(data)
        
    queryset.update(is_processed=True)
    modeladmin.message_user(request, "%s models successfully migrated." % queryset.count())        
migrate.short_description = "Migrate"

class BranchesAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'email', 'timezone', 'is_processed')    
    actions = (migrate,)
    
class VenuesAdmin(admin.ModelAdmin):
    list_display = ('title','is_processed')    
    actions = (migrate,)    

class TeachersAdmin(admin.ModelAdmin):
    list_display = ('fullname','is_processed')    
    actions = (migrate,)
        
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('title','is_processed')    
    actions = (migrate,)
    
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('fullname','is_processed')    
    actions = (migrate,)    

    # admin.site.register(BranchPages)
    # admin.site.register(BranchPhotos)
    # admin.site.register(BranchSeasons)
    # 
    # admin.site.register(Branches, BranchesAdmin)
    # admin.site.register(Venues, VenuesAdmin)
    # admin.site.register(Teachers, TeachersAdmin)
    # admin.site.register(Classes,ClassesAdmin)
    # admin.site.register(Students, StudentsAdmin)
    # 
    # admin.site.register(ClassCategories)
    # admin.site.register(ClassNotifications)
    # admin.site.register(ClassesXItems)
    # admin.site.register(Feedbacks)
    # admin.site.register(Items)
    # admin.site.register(Mailinglist)
    # admin.site.register(Notifications)
    # admin.site.register(NotificationsDefaults)
    # admin.site.register(StudentsXClasses)
    # admin.site.register(StudentsXItems)
    # admin.site.register(TeachersXClasses)
    # admin.site.register(Users)
    # admin.site.register(VenueRules)
    # admin.site.register(VenueRulesExceptions)
    # admin.site.register(VenueTimes)
