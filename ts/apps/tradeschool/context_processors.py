from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils import translation
from tradeschool.models import *

def branch(request):
    
    url = resolve(request.path)
    branch_slug = url.kwargs.get('branch_slug')
    
    try:
        
        if branch_slug == None and (url.app_name == 'admin' or url.app_name == 'rosetta') and request.user.is_staff:
            if request.user.branch_set.count() > 0:
                branch = request.user.branch_set.all()[0]
                translation.activate(branch.language)
            else:
                branch = Branch(timezone=settings.TIME_ZONE)

            return { 'branch' : branch, }
        
        branch = Branch.objects.get(slug=branch_slug)
        pages  = BranchPage.objects.filter(branch=branch) 
        
        translation.activate(branch.language)
        
        return { 'branch'       : branch, 
                 'branch_pages' : pages,
               }
        
    except Branch.DoesNotExist:
        branch = Branch(timezone=settings.TIME_ZONE)
        return { 'branch' : branch, }
         
   