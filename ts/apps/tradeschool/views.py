from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from tradeschool.models import *
from tradeschool.forms import *
from django.template.defaultfilters import slugify


def class_list(request, course_slug=None):
    schedules = Schedule.public.all()
    if course_slug != None:
        previewed_course = Course.objects.get(slug=course_slug)
    else:
        previewed_course = None
    
    return render_to_response('classes.html',{ 'schedules': schedules, 'previewed_course': previewed_course}, context_instance=RequestContext(request))


def class_register(request, course_slug=None):
    schedule             = get_object_or_404(Schedule, course__slug=course_slug)
    #open_seat_percentage = (schedule.registered_students / schedule.course.max_students) * 100;
    open_seat_percentage = 50
    #seats_left           = schedule.course.max_students - schedule.registered_students
    seats_left = 2 
    
    if request.method == 'POST':
        student_form          = StudentForm(request.POST, prefix="student")
        registered_item_forms = RegisteredItemForm(request.POST, prefix="item")        
                
        if registration_form.is_valid() and student_form.is_valid():
            current_site = Site.objects.get_current()
            
            # save student
            teacher = teacher_form.save(commit=False)
            teacher_data = teacher_form.cleaned_data
            teacher_data['slug'] = slugify(teacher.fullname)
            teacher, created = Person.objects.get_or_create(fullname=teacher.fullname, defaults=teacher_data)
            teacher.site.add(current_site)
            teacher.save()
                        
            # save registration
            #venue = Venue.objects.get(title="Cuchifritos")
            selected_time = time_form.cleaned_data['time']  
            schedule = Schedule(course=course, start_time=selected_time.start_time, end_time=selected_time.end_time, course_status=0)
            schedule.save()
            
            # save registered barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data
                barter_item = BarterItem(title=barter_item_form_data['title'], requested=barter_item_form_data['requested'], schedule=schedule)
                barter_item.save()
            
    else :            
        student_form         = StudentForm(prefix="student")
        registered_item_form = RegisteredItemForm(schedule=schedule, prefix="item")        
        
    return render_to_response(
        'register.html',
        {'schedule'             : schedule,
         'open_seat_percentage' : open_seat_percentage,
         'seats_left'           : seats_left,
         'registered_item_form' : registered_item_form,
         'student_form'         : student_form,}, 
        context_instance=RequestContext(request))
        

def teacher_info(request):    
    return render_to_response('teacher-info.html', {}, context_instance=RequestContext(request))

def past_classes(request):    
    return render_to_response('teacher-info.html', {}, context_instance=RequestContext(request))

def add_class(request):
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
            schedule = Schedule(course=course, start_time=selected_time.start_time, end_time=selected_time.end_time, course_status=0)
            schedule.save()
            
            # save barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data
                barter_item = BarterItem(title=barter_item_form_data['title'], requested=barter_item_form_data['requested'], schedule=schedule)
                barter_item.save()
            
    else :            
        BarterItemFormSet   = formset_factory(BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(prefix="item")
        course_form         = CourseForm(prefix="course")
        teacher_form        = TeacherForm(prefix="teacher")
        time_form           = TimeSelectionForm(prefix="time")
    
    return render_to_response(
        'add.html',
        {'barter_item_formset'  : barter_item_formset,
         'course_form'          : course_form,
         'teacher_form'         : teacher_form,
         'time_form'            : time_form,}, 
        context_instance=RequestContext(request))
