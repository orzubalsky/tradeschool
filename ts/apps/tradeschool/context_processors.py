from django.conf import settings
from django.core.urlresolvers import resolve
from tradeschool.models import *

def branch(request):
    
    url = resolve(request.path)
    branch_slug = url.kwargs.get('branch_slug')

    try:
        branch = Branch.objects.get(slug=branch_slug)
        pages  = BranchPage.objects.filter(branch=branch) 
                
        return { 'branch'       : branch, 
                 'branch_pages' : pages,
               }
        
    except Branch.DoesNotExist:
        return {}
