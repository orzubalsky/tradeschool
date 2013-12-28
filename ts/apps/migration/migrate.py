from migration.models import *
      
def migrate(modeladmin, queryset): 
    "create an intance of the tradeschool app model"  
    
    # iterate over selected rows
    for old_db_model in queryset:
        print "migrating %s" % (old_db_model.__name__)
        # get fields and values for each db row
        data = {k: v for k,v in old_db_model.__dict__.items()}

        # call the appropriate function, according to the rules dictionary
        modeladmin.model.migrate(data)
        
    queryset.update(is_processed=True)
    
migrate(Branches, Branches.objects.all())
migrate(Venues, Venues.objects.all())
migrate(Teachers, Teachers.objects.all())
migrate(Classes, Classes.objects.all())
migrate(Students, Students.objects.all())