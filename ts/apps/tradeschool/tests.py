"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from datetime import *
from tradeschool.models import *


class RegistrationTestCase(TestCase):
    """ test student registration """
    def setUp(self):
        self.client = Client()

        self.site     = Site(domain="http://test.tradeschool.coop/", name="test ts", id=2)
        self.site.save()
        
        self.branch   = Branch(title="test trade school", phone="123-123-1234", city="testown", country="US", slug="test", email="test@ts.coop", timezone="America/New_York", site=self.site)
        self.branch.save()
        
        self.venue    = Venue(title="test venue", phone="234-234-2345", city="testown", country="US", venue_type=0, address_1="123 test st", capacity=20, site=self.site)
        self.venue.save()
        
        self.teacher  = Person(fullname="test teacher", email="test@teacher.com", phone="123-123-1234", bio="test bio", website="http://test.com", slug="testteacher")
        self.teacher.save()
        
        self.course   = Course(teacher=self.teacher, category=0, max_students=20, title="test course", slug="testcourse", description="this a test class")
        self.course.save()
        
        self.schedule = Schedule(start_time=datetime(2020, 1, 31, 18, 00, 00), end_time=datetime(2020, 1, 31, 21, 00, 00), venue=self.venue, course=self.course, course_status=3, slug="test-course-01")    
        self.schedule.save()
    
    def test_registration(self):
        """
        """
        response = self.client.get(reverse('schedule-register', kwargs={ 'schedule_slug': self.schedule.slug }))        
        print response
        self.assertEqual(1 + 1, 2)
