from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


def branch_list(request):
    """ """
    from tradeschool.models import Branch, Schedule
    
    branches  = Branch.objects.all()
    schedules = Schedule.public.all()

    return render_to_response('branch_list.html',{ 'branches': branches, 'schedules' : schedules }, context_instance=RequestContext(request))