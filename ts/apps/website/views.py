from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from tradeschool.models import *
from tradeschool.forms import *

def index(request):   
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
