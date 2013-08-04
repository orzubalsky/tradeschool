from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from migration.models import *

def migrate(handle, model, branch_slug=None): 
    "create an intance of the tradeschool app model"  
    
    handle.stdout.write('\n\nstarting migration of %s \n\n' % model.__doc__)
      
    # iterate over selected rows
    queryset = model.objects.all()
    for old_db_model in queryset:
        # get fields and values for each db row
        data = {k: v for k,v in old_db_model.__dict__.items()}
        # call the appropriate function, according to the rules dictionary

        model.objects.migrate(data, branch_slug)
        handle.stdout.write('migrated %s: [%i] \n' % (old_db_model.__str__(), data['id']))
                
    #queryset.update(is_processed=True)
    
class Command(BaseCommand): 

    help = 'migrate the old tradeschool db to the new django based site'

    option_list = BaseCommand.option_list + (
        make_option('--branch_slug',
            #action='store_true',
            help='Branch slug field'),
    )
        
    def handle(self, *args, **kwargs):
        """ """
        branch_slug = None        
        if kwargs.get('branch_slug'):
            branch_slug = kwargs.get('branch_slug') 

        #migrate(self, Branches, branch_slug)
        #migrate(self, Venues, branch_slug)
        #migrate(self, Teachers, branch_slug)
        #migrate(self, Classes, branch_slug)
        migrate(self, Students, branch_slug)
        migrate(self, BranchPages, branch_slug)
        migrate(self, BranchPhotos, branch_slug)
        migrate(self, Feedbacks, branch_slug)
        migrate(self, Users, branch_slug)

