from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import *
from tradeschool.models import *


class Command(BaseCommand):
    help = 'send the unsent timed emails from the past hour'

    def handle(self, *args, **options):
        """ """
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=1, minutes=1)

        courses = Course.objects.filter(
            start_time__gte=(start_date - timedelta(days=14)),
            end_time__lte=(start_date + timedelta(days=14)),
            status='approved',
            is_active=True
        )

        self.stdout.write(
            'found %i courses in the next 14 days\n' % (courses.count())
        )

        for course in courses:
            result = course.send_timed_emails_in_range(start_date, end_date)
            self.stdout.write(
                '%i emails sent for: %s' % (result, course.title)
            )
