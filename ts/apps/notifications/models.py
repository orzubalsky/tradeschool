from django.db.models import *
from django.contrib.sites.models import Site
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
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('sent', 'Sent')
    )
    
    schedule     = ForeignKey(Schedule)
    send_on      = DateTimeField(blank=True, null=True)
    email_status = SmallIntegerField(max_length=1, choices=EMAIL_CHOICES)


class BranchNotificationTemplate(Email):
    """
    These are the initial templates that are used
    to generate a branch notification templates when a new branch is added.
    They should only be edited by super admins.
    """

    cron = BooleanField(verbose_name="timed email", help_text="Check this box if this email should get sent automatically") 


class BranchNotification(BranchNotificationTemplate):
    """
    These are the notification templates for a single branch.
    They are used to generate class notifications when a course is created.
    """

    site = ForeignKey(Site)
    
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
                
            
