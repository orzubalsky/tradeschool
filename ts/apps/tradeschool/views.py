from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.utils import simplejson as json
from tradeschool.models import *
from tradeschool.forms import *
from notifications.models import *



def schedule_list(request, schedule_slug=None):
    """ """
    schedules = Schedule.public.all()
    if schedule_slug != None:
        previewed_course = Course.objects.get(slug=schedule_slug)
    else:
        previewed_course = None
    
    return render_to_response('schedule_list.html',{ 'schedules': schedules, 'previewed_course': previewed_course}, context_instance=RequestContext(request))


def schedule_register(request, schedule_slug=None, data=None):
    """ """
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
           student_data['slug'] = slugify(student.fullname)
           student, created = Person.objects.get_or_create(fullname=student.fullname, defaults=student_data)
           student.site.add(current_site)
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
                
    return render_to_response('schedule_register.html', 
    {
        'schedule'             : schedule,
        'open_seat_percentage' : open_seat_percentage,
        'seats_left'           : seats_left,
        'registration_form'    : registration_form,
        'student_form'         : student_form,    
    }, context_instance=RequestContext(request), mimetype="application/json")
    

def teacher_info(request):    
    """ """
    return render_to_response('teacher-info.html', {}, context_instance=RequestContext(request))


def past_schedules(request):
    """ """ 
    schedules = Schedule.past.all()
    
    return render_to_response('schedule_list_past.html',{ 'schedules': schedules,}, context_instance=RequestContext(request))    


def schedule_add(request):
    """ """
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
            teacher_data['slug'] = slugify(teacher.fullname)
            teacher, created = Person.objects.get_or_create(fullname=teacher.fullname, defaults=teacher_data)
            teacher.site.add(current_site)
            teacher.save()

            # save course
            course  = course_form.save(commit=False)
            course_data = course_form.cleaned_data
            course_data['slug'] = slugify(course.title)
            course_data['teacher'] = teacher
            course, created = Course.objects.get_or_create(title=course.title, defaults=course_data)
            course.site.add(current_site)
            course.save()

            # save schedule
            #venue = Venue.objects.get(title="Cuchifritos")
            selected_time = time_form.cleaned_data['time']  
            schedule = Schedule(course=course, start_time=selected_time.start_time, end_time=selected_time.end_time, slug=slugify(course.title), course_status=0)
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
            return HttpResponseRedirect( reverse(schedule_submitted, args=[schedule.slug]) )            

    else :
        BarterItemFormSet   = formset_factory(BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(prefix="item")
        course_form         = CourseForm(prefix="course")
        teacher_form        = TeacherForm(prefix="teacher")
        time_form           = TimeSelectionForm(prefix="time")

    return render_to_response(
        'schedule_submit.html',
        {'barter_item_formset'  : barter_item_formset,
         'course_form'          : course_form,
         'teacher_form'         : teacher_form,
         'time_form'            : time_form,}, 
        context_instance=RequestContext(request))



def schedule_edit(request, schedule_slug=None):
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
            teacher.slug = slugify(teacher.fullname)
            teacher.save()
            
            # save course
            course = course_form.save(commit=False)
            course.slug = slugify(course.title)
            course.save()

            # save schedule
            schedule.slug = slugify(course.title)
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

    return render_to_response(
        'schedule_submit.html',
        {'barter_item_formset'  : barter_item_formset,
         'course_form'          : course_form,
         'teacher_form'         : teacher_form,}, 
        context_instance=RequestContext(request))    


def schedule_submitted(request, schedule_slug):
    """ loaded after a successful submission of the schedule form."""
    schedule = get_object_or_404(Schedule, slug=schedule_slug)
    
    return render_to_response('schedule_submitted.html', { 'schedule': schedule, }, context_instance=RequestContext(request))


def schedule_unregister(request, schedule_slug, student_slug):
    """ """
    registration = get_object_or_404(Registration, student__slug=student_slug, schedule__slug=schedule_slug)
    
    if request.method == 'POST':
        registration.registration_status = 'unregistered'
        registration.save()
        return HttpResponseRedirect( reverse(schedule_list,) )
        
    return render_to_response('schedule_unregister.html', { 'registration' : registration }, context_instance=RequestContext(request))


def schedule_feedback(request, schedule_slug=None, feedback_type='student'):
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
             return HttpResponseRedirect( reverse(schedule_list,) )            

    else :
        form = FeedbackForm()

    return render_to_response('schedule_feedback.html', {'form' : form,},  context_instance=RequestContext(request))    