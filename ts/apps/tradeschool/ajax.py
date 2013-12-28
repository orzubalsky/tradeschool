from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from tradeschool.views import *


@dajaxice_register(method='POST')
def course_load_form(request, branch_slug=None, course_slug=None):
    """
    """
    return course_register(request, branch_slug, course_slug)


@dajaxice_register(method='POST')
def course_submit_form(request, data, branch_slug=None, course_slug=None):
    """
    """
    return course_register(
        request,
        branch_slug,
        course_slug,
        deserialize_form(data)
    )
