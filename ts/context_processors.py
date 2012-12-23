from django.conf import settings
from django.contrib.sites.models import Site
from tradeschool.models import *

def site(request):
    site    = Site.objects.get_current()
    
    if settings.SITE_ID == 1:
        return { 'site': site, }
    else:
        branch  = Branch.objects.get(site__id__exact=site.pk)        
        return { 'site': site, 'branch':branch }        