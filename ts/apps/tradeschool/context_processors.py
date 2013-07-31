from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils import translation
from django.utils import timezone
from tradeschool.models import *

def branch(request):
    
    url = resolve(request.path)
    branch_slug = url.kwargs.get('branch_slug')
    
    
    
    try:
        
        if branch_slug == None and (url.app_name == 'admin' or url.app_name == 'rosetta') and request.user.is_staff:
            if request.user.branches.count() > 0:
                branch = Branch.objects.filter(organizers=request.user)[0]
                translation.activate(branch.language)
            else:
                branch = Branch(timezone=settings.TIME_ZONE)

            return { 'branch' : branch, }

        branch = Branch.objects.get(slug=branch_slug)
        
        translation.activate(branch.language)
        
        return { 'branch'       : branch, }
        
    except Branch.DoesNotExist:
        branch = Branch(timezone=settings.TIME_ZONE)
        return { 'branch' : branch, }
   