from django.contrib.sites.models import Site
from tradeschool.models import *

def site(request):
    site    = Site.objects.get_current()
    branch  = Branch.objects.get(site__id__exact=site.pk)
    
    return { 'site': site, 'branch':branch }