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
            # save teacher
            teacher = teacher_form.save(commit=False)
            teacher_data = teacher_form.cleaned_data
            teacher_data['slug'] = slugify(teacher.fullname)
            teacher, created = Person.objects.get_or_create(fullname=teacher.fullname, defaults=teacher_data)
            teacher.save()
            
            # save course
            course  = course_form.save(commit=False)
            course_data = course_form.cleaned_data
            course_data['slug'] = slugify(course.title)
            course_data['teacher'] = teacher
            course, created = Course.objects.get_or_create(title=course.title, defaults=course_data)
            course.save()
                        
            # save schedule
            venue = Venue.objects.get(title="Cuchifritos")
            selected_time = time_form.cleaned_data['time']  
            schedule = Schedule(course=course, start_time=selected_time.start_time, end_time=selected_time.end_time, venue=venue, course_status=0)
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
        teacher_form        = TeacherForm(prefix="teahcer")
        time_form           = TimeSelectionForm(prefix="time")
    
    return render_to_response(
        'add.html',
        {'barter_item_formset'  : barter_item_formset,
         'course_form'          : course_form,
         'teacher_form'         : teacher_form,
         'time_form'            : time_form,}, 
        context_instance=RequestContext(request))
