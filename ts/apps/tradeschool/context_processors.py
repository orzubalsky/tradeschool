from django.conf import settings
from django.core.urlresolvers import resolve
from tradeschool.models import *

def branch(request):
    
    url = resolve(request.path)
    branch_slug = url.kwargs.get('branch_slug')
    
    try:
        if branch_slug == None and (url.app_name == 'admin' or url.app_name == 'rosetta') and request.user.is_staff:
            # if the user is organizing at least one branch return the first one,
            # if not, create a branch with a timezone to pass to the template
            if request.user.branches_organized.count() > 0:
                branch = Branch.objects.filter(organizers=request.user)[0]
            else:
                branch = Branch(timezone=settings.TIME_ZONE)

            return { 'branch' : branch, }

        # if the request wasn't made to the admin or rosetta apps, 
        # we want to pass the branch to the template context
        # depending on the slug that was parsed from the URL
        branch = Branch.objects.get(slug=branch_slug)
        
        return { 'branch'       : branch, }
        
    except Branch.DoesNotExist:
        # when no branch exists, create one dynamically just so the timezone
        # can be passed to the template
        branch = Branch(timezone=settings.TIME_ZONE)
        return { 'branch' : branch, }
   