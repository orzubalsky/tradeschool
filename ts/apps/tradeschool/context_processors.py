from django.conf import settings
from tradeschool.models import *

def branch(request, branch_slug=None):
    try:
        branch = Branch.objects.get(slug=branch_slug)
        
        return { 'branch':branch }        
        
    except Branch.DoesNotExist:
        pass