
from django.test import TestCase

from tradeschool import models
from tradeschool.calendar import export


class CalendarExportTestCase(TestCase):

    def test_course_to_event(self):
        course = models.Course
        self.assertFalse(True) 
