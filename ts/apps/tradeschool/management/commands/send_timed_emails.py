from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
from datetime import * 
    
class Command(BaseCommand): 
    help = 'send the unsent timed emails from the past hour'
        
    def handle(self, *args, **options):
        """ """
        from ts.models import Schedule, ScheduleEmailContainer, TimedEmail, StudentReminder, StudentFeedback, TeacherReminder, TeacherFeedback
        
        end_date   = datetime.utcnow().replace(tzinfo=utc)
        start_date = end_date - timedelta(hours=1, minutes=1)

        schedules = Schedule.objects.filter(start_time__gte=(start_date - timedelta(days=14)), end_time__lte=(start_date + timedelta(days=14)))
        
        self.stdout.write('found %i schedules in the next 14 days\n' % (schedules.count()))
        
        for schedule in schedules:
            self.stdout.write('\n\n\niterating over emails in: %s\n' % (schedule.course.title))
            self.stdout.write('looking for emails within %s and %s\n' % (start_date, end_date))            
            try:
                for fieldname, email_obj in schedule.emails.emails.iteritems():
                    if isinstance(email_obj, TimedEmail):
                        self.stdout.write('email send on datetime: %s\n' % (email_obj.send_on))                        
                        if start_date < email_obj.send_on < end_date and email_obj.email_status == 'unsent':
                            self.stdout.write('email send on is within %s and %s\n' % (start_date, end_date))
                            if isinstance(email_obj, StudentReminder) or isinstance(email_obj, StudentFeedback):
                                for registration in schedule.registration_set.all():
                                    self.stdout.write('emailing student: %s at %s\n' % (registration.student.fullname, registration.student.email))
                                    email_obj.send(schedule, (registration.student.email,), registration)
                            if isinstance(email_obj, TeacherReminder) or isinstance(email_obj, TeacherFeedback):                                                                    
                                self.stdout.write('emailing teacher: %s at %s\n' % (schedule.course.teacher.fullname, schedule.course.teacher.email))                            
                                email_obj.send(schedule, (schedule.course.teacher.email,))
            except ScheduleEmailContainer.DoesNotExist:
                self.stdout.write('no emails found\n\n\n')
