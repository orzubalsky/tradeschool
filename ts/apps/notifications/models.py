from django.core.mail import send_mail
#from django_mailer import send_mail
from django.db.models import *
from django.contrib.sites.models import Site
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.template import Template
from tradeschool.models import Base, Branch, Course, Schedule


class Email(Base):
    """
    Abstract model for all email notifications in the ts system.
    TS-wide notification templates, individulal branch notification templates,
    and schedule-specific notification templates extend this model. 
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

    def preview(self, schedule_obj, registration=None):
        template = Template(self.content)
        context  = self.template_context(schedule_obj)
        body     = template.render(context)
        return body

    def send(self, schedule_obj, recipient, registration=None):
        body = self.preview(schedule_obj)
        site = Site.objects.get_current()
        send_mail(self.subject, body, site.branch.email, recipient)

    def template_context(self, schedule_obj, registration=None):
        """ """
        teacher = schedule_obj.course.teacher
        site    = Site.objects.get_current()
        branch  = Branch.objects.get(site=site)
        venue   = schedule_obj.venue
        domain  = site.domain
        
        student_feedback_url = "%s%s" % (domain, reverse('schedule-feedback-student', kwargs={'schedule_slug': schedule_obj.slug,}))
        teacher_feedback_url = "%s%s" % (domain, reverse('schedule-feedback-teacher', kwargs={'schedule_slug': schedule_obj.slug,}))
        class_edit_url       = "%s%s" % (domain, reverse('schedule-edit', kwargs={'schedule_slug': schedule_obj.slug,}))
        homepage_url         = "%s%s" % (domain, reverse('schedule-list'))

        student_list = ""
        for registration in schedule_obj.registration_set.all():
            student_list += "\n%s: " % registration.student.fullname
            student_items = []
            for item in registration.items.all():
                student_items.append(item.title)
            student_list += ", ".join(map(str, student_items))

        c = Context({
            'schedule'              : schedule_obj,
            'branch'                : branch,
            'teacher'               : teacher,
            'student_feedback_url'  : student_feedback_url,
            'teacher_feedback_url'  : teacher_feedback_url,
            'class_edit_url'        : class_edit_url,
            'homepage_url'          : homepage_url,
            'student_list'          : student_list
        })

        if registration != None:
            unregister_url = "%s%s" % (domain, reverse('schedule-unregister', kwargs={'schedule_slug': schedule_obj.slug, 'student_slug': registration.student.slug}))
            item_list = ""
            for item in registration.items.all():
                item_list += "%s\n" % item.title

            c.dicts.append({
                'student'       : registration.student,
                'registration'  : registration,
                'unregister_url': unregister_url,
                'item_list'     : item_list
            })

        return c

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
        
    branch = OneToOneField(Branch, related_name="emails")
    site   = OneToOneField(Site, related_name="emails")

    def __unicode__ (self):
        return u"for %s" % self.branch.title


class ScheduleEmailContainer(EmailContainer):
    """
    """
    class Meta:
        verbose_name = "Schedule Emails"
        verbose_name_plural = "Schedule Emails"
            
    schedule = OneToOneField(Schedule, related_name="emails")

    def email_teacher(self, email):
        """shortcut method to send an email via the ScheduleEmailContainer object."""
        return email.send(self.schedule, (self.schedule.course.teacher.email,))

    def email_student(self, email, registration):
        """shortcut method to send an email via the ScheduleEmailContainer object."""
        return email.send(self.schedule, (registration.student.email,), registration)
                        
    def email_students(self, email):
        """shortcut method to send an email via the ScheduleEmailContainer object."""
        for registration in self.schedule.registration_set.all():
            if registration.registration_status == 'registered':
                return self.email_student(email, registration)

    def preview(self, email):
        """shortcut method to preview an email via the ScheduleEmailContainer object."""
        return email.preview(self.schedule)

    def __unicode__ (self):
        return u"for %s" % self.schedule.course.title

