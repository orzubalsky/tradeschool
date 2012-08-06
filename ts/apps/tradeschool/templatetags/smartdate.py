from django import template
from django.template.defaultfilters import date as date_filter
import re

register = template.Library()

# --------------------------------------------------------------------------------
#   |smartdate:"date format" -- new arg 'c' (change) alteras the AM/pm appearance
# --------------------------------------------------------------------------------
@register.filter
def smartdate(value, arg):
    rendered = date_filter(value, arg)
    if 'c' in arg:
        rendered = re.sub('(a|p)\.m\.c', lambda m: '%sm' % m.group(1), rendered)
        rendered = re.sub('(A|P)Mc', lambda m: '%s.M.' % m.group(1), rendered)
    return rendered