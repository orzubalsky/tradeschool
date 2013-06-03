from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.utils import simplejson as json
from django.contrib.sites.models import get_current_site
from django.contrib.flatpages.views import render_flatpage
from tradeschool.utils import unique_slugify, branch_template
from tradeschool.models import *
from tradeschool.forms import *


def branch_list(request):
    """display all branches in current site."""
    
    branches  = Branch.objects.all()

    for branch in branches:
        branch.schedules = Schedule.public.filter(course__branch=branch)
        
    return render_to_response('hub/branch_list.html',{ 'branches': branches, }, context_instance=RequestContext(request))


def schedule_list(request, branch_slug=None, schedule_slug=None):
    """display all upcoming schedules for branch."""

    branch = get_object_or_404(Branch, slug=branch_slug)
    
    schedules = Schedule.public.filter(course__branch=branch)
    
    if schedule_slug != None:
        previewed_course = Schedule.objects.get(slug=schedule_slug)
    else:
        previewed_course = None
            
    template = branch_template(branch, 'schedule_list.html')
    
    return render_to_response(template.name ,{ 
            'schedules'         : schedules, 
            'previewed_course'  : previewed_course
        }, context_instance=RequestContext(request))


def schedule_register(request, branch_slug=None, schedule_slug=None, data=None):
    """ """
    branch               = get_object_or_404(Branch, slug=branch_slug)
    schedule             = get_object_or_404(Schedule, slug=schedule_slug)
    open_seat_percentage = round((float(schedule.registered_students) / float(schedule.course.max_students)) * 100);
    seats_left           = schedule.course.max_students - schedule.registered_students

    if data != None:
        student_form      = StudentForm(data=data, prefix="student")
        registration_form = RegistrationForm(data=data, schedule=schedule, prefix="item")        
   
        if registration_form.is_valid() and student_form.is_valid():
           current_site = Site.objects.get_current()
           
           # save student
           student = student_form.save(commit=False)
           student_data = student_form.cleaned_data
           student_data['slug'] = unique_slugify(Student, student.fullname)
           student, created = Person.objects.get_or_create(fullname=student.fullname, defaults=student_data)
           student.branch.add(branch)
           student.save()
                       
           # save registration
           registration = registration_form.save(commit=False)
           registration.student = student
           registration.schedule = schedule
           registration.save()

           # save items in registration through RegisteredItem
           for barter_item in registration_form.cleaned_data['items']:
               registered_item = RegisteredItem(registration=registration, barter_item=barter_item)
               registered_item.save()
   
           # email confirmation to student
           schedule.emails.email_student(schedule.emails.student_confirmation, registration)
           
           # render thank you template
           return render_to_response('schedule_registered.html', { 'registration' : registration, }, context_instance=RequestContext(request), mimetype="application/json")    

    else :            
        student_form      = StudentForm(prefix="student")
        registration_form = RegistrationForm(schedule=schedule, prefix="item")
    
    # return content as either json or html depending on request type
    if request.is_ajax():
        mimetype = "application/json"
    else:
        mimetype = "text/html"
        
    template = branch_template(branch, 'schedule_register.html')
    
    return render_to_response(template.name, 
    {
        'branch'               : branch,
        'schedule'             : schedule,
        'open_seat_percentage' : open_seat_percentage,
        'seats_left'           : seats_left,
        'registration_form'    : registration_form,
        'student_form'         : student_form,    
    }, context_instance=RequestContext(request), mimetype=mimetype)
    

def teacher_info(request, branch_slug=None):    
    """display a content page with information for prospective teachers. This page leads to the class submission form page."""
    
    branch = get_object_or_404(Branch, slug=branch_slug)
    
    template = branch_template(branch, 'teacher-info.html')    
    
    return render_to_response(template.name, { 'branch' : branch, }, context_instance=RequestContext(request))


def past_schedules(request, branch_slug=None):
    """display a list of past classes for the current branch."""

    branch = get_object_or_404(Branch, slug=branch_slug)
    
    schedules = Schedule.past.all()
    
    template = branch_template(branch, 'schedule_list_past.html')        
    
    return render_to_response(template.name,{ 
            'branch'    : branch,
            'schedules' : schedules,
        }, context_instance=RequestContext(request))    


def schedule_add(request, branch_slug=None):
    """ """
    
    branch = get_object_or_404(Branch, slug=branch_slug)
    
    if request.method == 'POST':
        BarterItemFormSet   = formset_factory(BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(request.POST, prefix="item")
        course_form         = CourseForm(request.POST, prefix="course")
        teacher_form        = TeacherForm(request.POST, prefix="teacher")
        time_form           = TimeSelectionForm(request.POST, prefix="time")
                
        if barter_item_formset.is_valid() and course_form.is_valid() and teacher_form.is_valid() and time_form.is_valid():
            current_site = Site.objects.get_current()
            
            # save teacher
            teacher = teacher_form.save(commit=False)
            teacher_data = teacher_form.cleaned_data
            teacher_data['slug'] = unique_slugify(Teacher, teacher.fullname)
            teacher, created = Person.objects.get_or_create(fullname=teacher.fullname, defaults=teacher_data)
            teacher.branch.add(branch)
            teacher.save()

            # save course
            course  = course_form.save(commit=False)
            course_data = course_form.cleaned_data
            course_data['slug'] = unique_slugify(Course, course.title)
            course_data['teacher'] = teacher
            course, created = Course.objects.get_or_create(title=course.title, defaults=course_data)
            course.branch.add(branch)
            course.save()

            # save schedule
            selected_time = time_form.cleaned_data['time']
            schedule = Schedule(course=course, start_time=selected_time.start_time, end_time=selected_time.end_time, course_status=0)
            schedule.slug = unique_slugify(Schedule, course.title)
            if selected_time.venue is not None:
                schedule.venue = selected_time.venue
            schedule.save()

            # save barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data
                barter_item = BarterItem(title=barter_item_form_data['title'], requested=barter_item_form_data['requested'], schedule=schedule)
                barter_item.save()

            # send confirmation email to teacher
            schedule.emails.email_teacher(schedule.emails.teacher_confirmation)

            # delete the selected time slot
            Time.objects.get(pk=selected_time.pk).delete()
            
            # redirect to thank you page
            return HttpResponseRedirect( reverse(schedule_submitted, kwargs={'schedule_slug' : schedule.slug, 'branch_slug': branch.slug}))            

    else :
        BarterItemFormSet   = formset_factory(BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(prefix="item")
        course_form         = CourseForm(prefix="course")
        teacher_form        = TeacherForm(prefix="teacher")
        time_form           = TimeSelectionForm(prefix="time")

    template = branch_template(branch, 'schedule_submit.html')

    return render_to_response(template.name, {
            'branch'               : branch,
            'barter_item_formset'  : barter_item_formset,
            'course_form'          : course_form,
            'teacher_form'         : teacher_form,
            'time_form'            : time_form,
        }, 
        context_instance=RequestContext(request))



def schedule_edit(request, schedule_slug=None, branch_slug=None):
    """ """
    schedule = get_object_or_404(Schedule, slug=schedule_slug)
    
    if request.method == 'POST':
        BarterItemFormSet   = formset_factory(BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(request.POST, prefix="item")
        course_form         = CourseForm(request.POST, prefix="course", instance=schedule.course)
        teacher_form        = TeacherForm(request.POST, prefix="teacher", instance=schedule.course.teacher)

        if barter_item_formset.is_valid() and course_form.is_valid() and teacher_form.is_valid():
            current_site = Site.objects.get_current()

            # save teacher
            teacher = teacher_form.save(commit=False)
            teacher.slug = unique_slugify(Teacher, teacher.fullname)
            teacher.save()
            
            # save course
            course = course_form.save(commit=False)
            course.slug = unique_slugify(Course, course.title)
            course.save()

            # save schedule
            schedule.slug = unique_slugify(Schedule, course.title)
            schedule.save()

            # save barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data
                barter_item, created = BarterItem.objects.get_or_create(title=barter_item_form_data['title'], requested=barter_item_form_data['requested'], schedule=schedule)
                barter_item.save()

            return HttpResponseRedirect( reverse(schedule_submitted, args=[schedule.slug]) )

    else :
        initial_item_data = []
        for item in schedule.barteritem_set.all():
            initial_item_data.append({'title':item.title, 'requested':item.requested})

        BarterItemFormSet   = formset_factory(BarterItemForm, extra=0, formset=BaseBarterItemFormSet,)
        barter_item_formset = BarterItemFormSet(prefix="item", initial=initial_item_data)
        course_form         = CourseForm(prefix="course", instance=schedule.course)
        teacher_form        = TeacherForm(prefix="teacher", instance=schedule.course.teacher)

    template = branch_template(branch, 'schedule_submit.html')
    
    return render_to_response(template.name, {
        'barter_item_formset'  : barter_item_formset,
        'course_form'          : course_form,
        'teacher_form'         : teacher_form, 
    },context_instance=RequestContext(request))    


def schedule_submitted(request, schedule_slug=None, branch_slug=None):
    """ loaded after a successful submission of the schedule form."""
    
    schedule = get_object_or_404(Schedule, slug=schedule_slug)
    
    template = branch_template(branch, 'schedule_submitted.html')
        
    return render_to_response(template.name, { 'schedule': schedule, }, context_instance=RequestContext(request))


def schedule_unregister(request, branch_slug=None, schedule_slug=None, student_slug=None):
    """ """
    registration = get_object_or_404(Registration, student__slug=student_slug, schedule__slug=schedule_slug)
    
    if request.method == 'POST':
        registration.registration_status = 'unregistered'
        registration.save()
        return HttpResponseRedirect( reverse(schedule_list,kwargs={'branch_slug' : branch_slug,}) )

    template = branch_template(branch, 'schedule_unregister.html')
        
    return render_to_response(template.name, { 'registration' : registration }, context_instance=RequestContext(request))


def schedule_feedback(request, branch_slug=None, schedule_slug=None, feedback_type='student'):
    """ """
    schedule = get_object_or_404(Schedule, slug=schedule_slug)
    
    if request.method == 'POST':
         form = FeedbackForm(data=request.POST)

         if form.is_valid():

             # save feedback
             feedback = form.save(commit=False)
             feedback.feedback_type = feedback_type
             feedback.schedule = schedule
             feedback.save()

             # redirect to thank you page
             return HttpResponseRedirect( reverse(schedule_list, kwargs={'branch_slug' : branch_slug, }) )            

    else :
        form = FeedbackForm()
    
    template = branch_template(branch, 'schedule_feedback.html')
    
    return render_to_response(template.name, {'form' : form,},  context_instance=RequestContext(request))    
    

def branchpage(request, url, branch_slug=None):
    """this is copied from django.contrib.flatpages.views only in order to 
       query the BranchPage table instead of FlatPage."""
        
    if not url.startswith('/'):
        url = '/' + url
    
    try:
        branch_page = get_object_or_404(BranchPage, url__exact=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            branch_page = get_object_or_404(BranchPage, url__exact=url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
            
    return render_flatpage(request, branch_page)