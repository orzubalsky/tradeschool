from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson as json
from django.utils.safestring import mark_safe
from django.core.mail import mail_admins, send_mail
from django.core.cache import cache
from tradeschool.forms import *


@dajaxice_register(method='POST')
def schedule_form(request, schedule_slug=None):
    """ """
    
    schedule             = get_object_or_404(Schedule, slug=schedule_slug)
    open_seat_percentage = round((float(schedule.registered_students) / float(schedule.course.max_students)) * 100);
    seats_left           = schedule.course.max_students - schedule.registered_students
    
    if request.method == 'POST':
        
        student_form      = StudentForm(data=request.POST, prefix="student")
        registration_form = RegistrationForm(data=request.POST, schedule=schedule, prefix="item")        
                
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
            
    else :            
        student_form      = StudentForm(prefix="student")
        registration_form = RegistrationForm(schedule=schedule, prefix="item")
    
    html = render_to_string('schedule_register.html', 
        {'schedule'             : schedule,
         'open_seat_percentage' : open_seat_percentage,
         'seats_left'           : seats_left,
         'registration_form'    : registration_form,
         'student_form'         : student_form,},
             )
    
    return json.dumps({'success': True, 'html': html})