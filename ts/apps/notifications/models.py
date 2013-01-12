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

    EMAIL_CHOICES = (
        ('disabled', 'Disabled'),
        ('not_sent', 'Not Sent Yet'),
        ('sent', 'Sent')
    )
    
    subject      = CharField(max_length=140)
    content      = TextField()
    email_status = CharField(max_length=30, choices=EMAIL_CHOICES, default='not_sent')
    
    def send(self, request):
        template = Template(self.template.content)
        context  = notification_template_context(self, request)
        print template.render(context)
        #print send_mail('Welcome to My Project', t.render(c), 'from@address.com', ('email@aa.com',), fail_silently=False)        

    def __unicode__ (self):
        return self.content


class TimedEmail(Email):
    """
    Abstract model for all email notifications in the ts system.
    TS-wide notification templates, individulal branch notification templates,
    and course-specific notification templates extend this model. 
    """
    class Meta:
            abstract = True
    
    send_on      = DateTimeField(blank=True, null=True)


class StudentConfirmation(Email):
    pass


class StudentReminder(TimedEmail):
    pass


class StudentFeedback(TimedEmail):
    pass
    
    
class TeacherConfirmation(Email):
    pass
    

class TeacherClassApproval(Email):
    pass                                 


class TeacherReminder(TimedEmail):
    pass


class TeacherFeedback(TimedEmail):
    pass


class EmailContainer(Base):
    """
    """
    class Meta:
        abstract = True
            
    student_confirmation   = ForeignKey(StudentConfirmation)
    student_reminder       = ForeignKey(StudentReminder)
    student_feedback       = ForeignKey(StudentFeedback)
    teacher_confirmation   = ForeignKey(TeacherConfirmation)
    teacher_class_approval = ForeignKey(TeacherClassApproval)
    teacher_reminder       = ForeignKey(TeacherReminder)
    teacher_feedback       = ForeignKey(TeacherFeedback)

    def emails():
        def fget(self):
            return {"student_confirmation"   : self.student_confirmation, 
                    "student_reminder"       : self.student_reminder, 
                    "student_feedback"       : self.student_feedback,
                    "teacher_confirmation"   : self.teacher_confirmation, 
                    "teacher_class_approval" : self.teacher_class_approval, 
                    "teacher_reminder"       : self.teacher_reminder, 
                    "teacher_feedback"       : self.teacher_feedback
                    }
        return locals()

    emails = property(**emails())


class DefaultEmailContainer(EmailContainer):
    """
    """


class BranchEmailContainer(EmailContainer):
    """
    """
    class Meta:
        verbose_name = "Branch Emails"
        verbose_name_plural = "Branch Emails"
        
    branch = ForeignKey(Branch, related_name="emails")
    site   = ForeignKey(Site, related_name="emails")

    def __unicode__ (self):
        return u"for %s" % self.branch.title


class ScheduleEmailContainer(EmailContainer):
    """
    """
    class Meta:
        verbose_name = "Schedule Emails"
        verbose_name_plural = "Schedule Emails"
            
    schedule = ForeignKey(Schedule, related_name="emails")

    def __unicode__ (self):
        return u"for %s" % self.schedule.course.title


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