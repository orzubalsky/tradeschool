from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import * 
from tradeschool.models import *
    
class Command(BaseCommand): 
    help = 'send the unsent timed emails from the past hour'
        
    def handle(self, *args, **options):
        """ """
        end_date   = timezone.now()
        start_date = end_date - timedelta(hours=1, minutes=1)

        schedules = Schedule.objects.filter(start_time__gte=(start_date - timedelta(days=14)), end_time__lte=(start_date + timedelta(days=14)))

        self.stdout.write('found %i schedules in the next 14 days\n' % (schedules.count()))
        
        for schedule in schedules:
            result = schedule.send_timed_emails_in_range(start_date, end_date)
            self.stdout.write('%i emails sent for: %s' % (result, schedule.course.title))