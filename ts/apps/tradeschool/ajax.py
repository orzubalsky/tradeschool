from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from tradeschool.views import *


@dajaxice_register(method='POST')
def schedule_load_form(request, branch_slug=None, schedule_slug=None):
    """ """
    return schedule_register(request, branch_slug, schedule_slug)
    
    
@dajaxice_register(method='POST')
def schedule_submit_form(request, data, schedule_slug=None):
    """ """
    return schedule_register(request, schedule_slug, deserialize_form(data))
