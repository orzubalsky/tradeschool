from django.utils import timezone
from django.core.urlresolvers import resolve
from tradeschool.models import *

class BranchMiddleware(object):
    def process_request(self, request):
        
        url = resolve(request.path)
        branch_slug = url.kwargs.get('branch_slug')

        try:
           if branch_slug == None and (url.app_name == 'admin' or url.app_name == 'rosetta') and request.user.is_staff:
               if request.user.branches.count() > 0:
                   branch = Branch.objects.filter(organizers=request.user)[0]
                   timezone.activate(branch.timezone)
               else:
                   pass

           branch = Branch.objects.get(slug=branch_slug)
           timezone.activate(branch.timezone)                        

        except Branch.DoesNotExist:
            pass