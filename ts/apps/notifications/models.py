from django.db.models import *
from django.contrib.sites.models import Site
from django.template import loader, Context
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import Template
from tradeschool.models import Base, Branch, Course, Schedule


class Email(Base):
    """
    Abstract model for all email notifications in the ts system.
    TS-wide notification templates, individulal branch notification templates,
    and course-specific notification templates extend this model. 
    """
    class Meta:
            abstract = True

    TYPE_CHOICES = (
        ('student_confirmation', 'Student Confirmation'),
        ('student_reminder', 'Student Reminder'),
        ('student_feedback', 'Student Feedback'),                
        ('teacher_confirmation', 'Teacher Confirmation'),
        ('teacher_class_approved', 'Teacher Class Approved'),                
        ('teacher_reminder', 'Teacher Reminder'),
        ('teacher_feedback', 'Teacher Feedback'),
    )    


    subject    = CharField(max_length=140)    
    content    = TextField()
    email_type = CharField(max_length=30, choices=TYPE_CHOICES) 
    
    def __unicode__ (self):
        return self.subject


class ScheduleNotification(Email):
    """
    Course notifications are sent to students and teachers on several occasions
    (see the email abstract model for a listing of the various notification types)
    When a course is created, the course notifications are generated for it.
    This is done because some course notification would have to be specific for the course.
    For example, a yoga course student reminder would include details about what to wear.
    """

    EMAIL_CHOICES = (
        ('disabled', 'Disabled'),
        ('not_sent', 'Not Sent Yet'),
        ('sent', 'Sent')
    )

    schedule     = ForeignKey(Schedule, related_name="notifications")
    send_on      = DateTimeField(blank=True, null=True)
    email_status = CharField(max_length=30, choices=EMAIL_CHOICES, default='not_sent')

    def send_teacer_confirmation(self, request):
        template = Template(self.content)
        context  = notification_template_context(self, request)
        print template.render(context)
        #print send_mail('Welcome to My Project', t.render(c), 'from@address.com', ('email@aa.com',), fail_silently=False)        


def notification_template_context(obj, request, registration=None):
    """ """
    teacher = obj.schedule.course.teacher
    branch  = Branch.objects.get(site=Site.objects.get_current())
    venue   = obj.schedule.venue

    student_feedback_url = reverse('schedule-feedback-student', kwargs={'schedule_slug': obj.schedule.slug,})
    student_feedback_url = request.build_absolute_uri(student_feedback_url)
    teacher_feedback_url = reverse('schedule-feedback-teacher', kwargs={'schedule_slug': obj.schedule.slug,})
    teacher_feedback_url = request.build_absolute_uri(teacher_feedback_url)
    class_edit_url       = reverse('schedule-edit', kwargs={'schedule_slug': obj.schedule.slug,})
    class_edit_url       = request.build_absolute_uri(class_edit_url)
    homepage_url         = reverse('schedule-list')
    homepage_url         = request.build_absolute_uri(homepage_url)
        
    student_list = ""
    for registration in obj.schedule.registration_set.all():
        student_list += "\n%s: " % registration.student.fullname
        student_items = []
        for item in registration.items.all():
            student_items.append(item.title)
        student_list += ", ".join(map(str, student_items))
    
    c = Context({
        'schedule'              : obj.schedule,
        'branch'                : branch,
        'teacher'               : teacher,
        'student_feedback_url'  : student_feedback_url,
        'teacher_feedback_url'  : teacher_feedback_url,
        'class_edit_url'        : class_edit_url,
        'homepage_url'          : homepage_url,
        'student_list'          : student_list
    })
        
    if registration != None:
        unregister_url = reverse('class-unregister', kwargs={'schedule_slug': obj.schedule.slug, 'student_slug': registration.student.slug})
        unregister_url = request.build_absolute_uri(unregister_url)
        item_list = ""
        for item in registration.items.all():
            item_list += "%s" % item.title    

        c.dicts.append({
            'student'       : student,
            'registration'  : registration,
            'unregister_url': unregister_url,
        })

    return c
        
            
class BranchNotificationTemplate(Email):
    """
    These are the initial templates that are used
    to generate a branch notification templates when a new branch is added.
    They should only be edited by super admins.
    """

    cron = BooleanField(verbose_name="timed email", help_text="Check this box if this email should get sent automatically") 


class BranchNotification(Email):
    """
    These are the notification templates for a single branch.
    They are used to generate class notifications when a course is created.
    """

    cron    = BooleanField(verbose_name="timed email", help_text="Check this box if this email should get sent automatically") 
    site    = ForeignKey(Site)
    branch  = ForeignKey(Branch, related_name="notifications")
    
    def calculate_send_time(self, schedule):
        if self.cron:
            if self.email_type == 'student_reminder':
                return schedule.start_time
            if self.email_type == 'student_feedback':
                return schedule.end_time
            if self.email_type == 'teacher_reminder':
                return schedule.start_time
            if self.email_type == 'teacher_feedback':
                return schedule.end_time