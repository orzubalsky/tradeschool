from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.utils import simplejson as json
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.contrib.sites.models import get_current_site
from django.contrib.flatpages.views import render_flatpage
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from tradeschool.utils import unique_slugify, branch_template, branch_templates
from tradeschool.models import *
from tradeschool.forms import *
from datetime import datetime, timedelta

def branch_list(request):
    """display all branches in current site."""
    
    branches  = Branch.objects.all()

    for branch in branches:
        branch.schedules = Schedule.public.filter(course__branch=branch)
        
    return render_to_response('hub/branch_list.html',{ 
            'branches': branches, 
        }, context_instance=RequestContext(request))


def schedule_list(request, branch_slug=None, schedule_slug=None):
    """display all upcoming schedules for branch."""

    branch = get_object_or_404(Branch, slug=branch_slug)
    
    schedules = Schedule.public.filter(course__branch=branch)
    
    branch_pages = BranchPage.objects.filter(branch=branch, is_visible=1)
    
    if schedule_slug != None:
        previewed_course = Schedule.objects.get(slug=schedule_slug)
    else:
        previewed_course = None
    
    view_templates = branch_templates(branch, 'schedule_list.html', 'base.html')
    
    return render_to_response(view_templates.template.name ,{ 
            'schedules'         : schedules,
            'previewed_course'  : previewed_course,
            'templates'         : view_templates,
            'branch_pages'      : branch_pages                    
        }, context_instance=RequestContext(request))


def redirect_to_schedule_list(request, branch_slug=None):
    """
    """
    return HttpResponseRedirect( reverse(schedule_list, kwargs={'branch_slug': branch_slug, }))


def schedule_register(request, branch_slug=None, schedule_slug=None, data=None):
    """ """
    branch               = get_object_or_404(Branch, slug=branch_slug)
    schedule             = get_object_or_404(Schedule, slug=schedule_slug)
    open_seat_percentage = round((float(schedule.registered_students) / float(schedule.course.max_students)) * 100);
    seats_left           = schedule.course.max_students - schedule.registered_students

    if request.method == 'POST' and not request.is_ajax():
        data = request.POST

    if data != None or request.method == 'POST':
        student_form      = StudentForm(data=data, prefix="student")
        registration_form = RegistrationForm(data=data, schedule=schedule, prefix="item")        
   
        if registration_form.is_valid() and student_form.is_valid():
            # save student
            student = student_form.save(commit=False)
            student_data = student_form.cleaned_data
            student_data['slug'] = unique_slugify(Student, student.fullname)
            student, created = Person.objects.get_or_create(email=student.email, defaults=student_data)
            student.branch.add(branch)
            student.save()
           
            # save registration
            registration = registration_form.save(commit=False)
            registration.student = student
            registration.schedule = schedule
            
            # try saving the registration. 
            # this may fail because of the unique_together db constraint on student and schedule fields
            # if this Student is registered to this Schedule an IntegrityError will occur
            try:
                registration.save()

                # save items in registration through RegisteredItem
                for barter_item in registration_form.cleaned_data['items']:
                    registration.items.add(barter_item)

                registration.save()
                
                # email confirmation to student
                schedule.emails.email_student(schedule.emails.student_confirmation, registration)

                # render thank you template
                view_templates = branch_templates(branch, 'schedule_registered.html', 'base.html')           
                return render_to_response(view_templates.template.name, {
                        'registration' : registration, 
                        'templates' : view_templates 
                    }, context_instance=RequestContext(request), mimetype="application/json")    

            # in case saving the registration failed (see comment above the try block),
            # add an error to the registration form
            except IntegrityError:
                registration_form._errors['items'] = registration_form.error_class([_('You are already registered to this class')])

    else :            
        student_form      = StudentForm(prefix="student")
        registration_form = RegistrationForm(schedule=schedule, prefix="item")
    
    # return content as either json or html depending on request type
    if request.is_ajax():
        view_templates = branch_templates(branch, 'schedule_register.html', 'base_ajax.html')
        popup_container_class = ''
        mimetype = "application/json"
    else:
        view_templates = branch_templates(branch, 'schedule_register.html', 'base.html')
        popup_container_class = 'visible'
        mimetype = "text/html"
    
    return render_to_response(view_templates.template.name, {
            'branch'               : branch,
            'schedule'             : schedule,
            'open_seat_percentage' : open_seat_percentage,
            'seats_left'           : seats_left,
            'registration_form'    : registration_form,
            'student_form'         : student_form,    
            'templates'            : view_templates,
            'popup_container_class': popup_container_class 
        }, context_instance=RequestContext(request), mimetype=mimetype)
    

def teacher_info(request, branch_slug=None):    
    """display a content page with information for prospective teachers. This page leads to the class submission form page."""
    
    branch = get_object_or_404(Branch, slug=branch_slug)
    
    view_templates = branch_templates(branch, 'teacher-info.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
            'branch'            : branch, 
            'templates'            : view_templates
        }, context_instance=RequestContext(request))


def schedule_list_past(request, branch_slug=None):
    """display a list of past classes for the current branch."""

    branch = get_object_or_404(Branch, slug=branch_slug)
    
    schedules = Schedule.past.all()
    
    view_templates = branch_templates(branch, 'schedule_list_past.html', 'subpage.html')    
    
    return render_to_response(view_templates.template.name,{ 
            'branch'    : branch,
            'schedules' : schedules,
            'templates' : view_templates
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
            
            # process teacher
            teacher = teacher_form.save(commit=False)
            teacher_data = teacher_form.cleaned_data
            
            # check if the submitting teacher already exists in the system
            # we determine an existing teacher by their email
            teacher, teacher_created = Person.objects.get_or_create(email=teacher.email, defaults=teacher_data)
            
            # if this is an existing teacher, update the field with the data from the form
            if not teacher_created:
                teacher.fullname = teacher_form.cleaned_data['fullname']
                teacher.bio      = teacher_form.cleaned_data['bio']
                teacher.website  = teacher_form.cleaned_data['website']
                teacher.phone    = teacher_form.cleaned_data['phone']                                                

            # create a slug for the teacher object
            teacher_data['slug'] = unique_slugify(Teacher, teacher.fullname)                

            # add a teacher-branch relationship to the current branch
            teacher.branch.add(branch)
            
            # save teacher
            teacher.save()

            # process course
            course  = course_form.save(commit=False)
            course_data = course_form.cleaned_data

            # create a slug for the course object                
            course_data['slug'] = unique_slugify(Course, course.title)
            
            # add the teacher as a foreign key
            course_data['teacher'] = teacher

            # check if the submited course already exists in the system
            # we determine an existing course by its title
            course, course_created = Course.objects.get_or_create(title=course.title, defaults=course_data)
            
            # if this is an existing course, update the field with the data from the form
            if not course_created:
                course.title        = course_form.cleaned_data['title']
                course.description  = course_form.cleaned_data['description']
                course.max_students = course_form.cleaned_data['max_students']
            
            # add a course-branch relationship to the current branch
            course.branch.add(branch)
            
            # save course
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
                
                # check if the submited barter item already exists in the system
                # we determine an existing barter item by its title
                barter_item, barter_item_created = BarterItem.objects.get_or_create(title=barter_item_form_data['title'], schedule=schedule, defaults=barter_item_form_data)                
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

    view_templates = branch_templates(branch, 'schedule_submit.html', 'subpage.html')    

    return render_to_response(view_templates.template.name, {
            'branch'               : branch,
            'barter_item_formset'  : barter_item_formset,
            'course_form'          : course_form,
            'teacher_form'         : teacher_form,
            'time_form'            : time_form,
            'templates'            : view_templates
        }, context_instance=RequestContext(request))



def schedule_edit(request, schedule_slug=None, branch_slug=None):
    """ """
    schedule = get_object_or_404(Schedule, slug=schedule_slug)
    branch   = get_object_or_404(Branch, slug=branch_slug)
    
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
            
            # remove all barter item relationships before saving them again
            for item in schedule.barteritem_set.all():
                item.delete()

            # save updated barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data
                barter_item, created = BarterItem.objects.get_or_create(title=barter_item_form_data['title'], schedule=schedule, defaults=barter_item_form_data)
                barter_item.save()
            return HttpResponseRedirect( reverse(schedule_submitted, kwargs={'branch_slug': branch.slug, 'schedule_slug': schedule.slug} ))

    else :
        initial_item_data = []
        for item in schedule.barteritem_set.all():
            initial_item_data.append({'title':item.title, })

        BarterItemFormSet   = formset_factory(BarterItemForm, extra=0, formset=BaseBarterItemFormSet,)
        barter_item_formset = BarterItemFormSet(prefix="item", initial=initial_item_data)
        course_form         = CourseForm(prefix="course", instance=schedule.course)
        teacher_form        = TeacherForm(prefix="teacher", instance=schedule.course.teacher)
    
    view_templates = branch_templates(branch, 'schedule_submit.html', 'subpage.html')    

    return render_to_response(view_templates.template.name, {
            'barter_item_formset'  : barter_item_formset,
            'course_form'          : course_form,
            'teacher_form'         : teacher_form,
            'templates'            : view_templates
        },context_instance=RequestContext(request))


def schedule_submitted(request, schedule_slug=None, branch_slug=None):
    """ loaded after a successful submission of the schedule form."""
    
    schedule = get_object_or_404(Schedule, slug=schedule_slug)
    branch   = get_object_or_404(Branch, slug=branch_slug)

    view_templates = branch_templates(branch, 'schedule_submitted.html', 'subpage.html')    
        
    return render_to_response(view_templates.template.name, {
            'schedule'          : schedule,
            'templates'         : view_templates
        }, context_instance=RequestContext(request))


def schedule_unregister(request, branch_slug=None, schedule_slug=None, student_slug=None):
    """ """
    registration = get_object_or_404(Registration, student__slug=student_slug, schedule__slug=schedule_slug)
    branch       = get_object_or_404(Branch, slug=branch_slug)
    
    if request.method == 'POST':        
        registration.registration_status = 'unregistered'
        registration.save()
        return HttpResponseRedirect( reverse(schedule_list,kwargs={'branch_slug' : branch_slug,}) )

    view_templates = branch_templates(branch, 'schedule_unregister.html', 'subpage.html')    
        
    return render_to_response(view_templates.template.name, {
            'registration'      : registration,
            'templates'         : view_templates
        }, context_instance=RequestContext(request))


def schedule_feedback(request, branch_slug=None, schedule_slug=None, feedback_type='student'):
    """ """
    # don't display form unless schedule is approved
    schedule = get_object_or_404(Schedule, slug=schedule_slug, course_status=3)
    branch   = get_object_or_404(Branch, slug=branch_slug)

    # don't display form unless the scheduled class took place
    if schedule.is_past == False:
        raise Http404

    if request.method == 'POST' and schedule.is_past:
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
    
    view_templates = branch_templates(branch, 'schedule_feedback.html', 'subpage.html')    
    
    return render_to_response(view_templates.template.name, {
            'form'              : form,
            'templates'         : view_templates
        },context_instance=RequestContext(request))    
    

def branch_page(request, url, branch_slug=None):
    """this is copied from django.contrib.flatpages.views only in order to 
       query the BranchPage table instead of FlatPage."""
        
    if not url.startswith('/'):
        url = '/' + url
    
    try:
        branch_page = get_object_or_404(BranchPage, url__exact=url, is_active=True)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            branch_page = get_object_or_404(BranchPage, url__exact=url, is_active=True)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
            
    return render_flatpage(request, branch_page)