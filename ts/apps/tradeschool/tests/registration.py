from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.conf import settings
from datetime import *
import shutil, os, os.path
from tradeschool.models import *



class RegistrationTestCase(TestCase):
    """ Tests the process of registering and unregistering to a schedule using the frontend forms.
    """
    fixtures = ['test_data.json', 'test_schedule.json']
    
    def setUp(self):
        """ 
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'
        
        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()

        self.schedule = Schedule.objects.filter(course__branch=self.branch)[0]

        self.url = reverse('schedule-register', kwargs={'branch_slug': self.branch.slug, 'schedule_slug': self.schedule.slug })


    def test_view_is_loading(self):
        """ Tests that the schedule-register view loads with the correct template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_register.html')


    def test_registration_empty_form(self):
        """ 
        """
        data = {}
        
        # post an empty form
        response = self.client.post(self.url, data=data, follow=True)
        
        # an empty form should return 3 errors for the required fields
        self.assertContains(response, 'Please', count=3)


    def test_capacity(self):
        """ Tests that the Join button is only visible if there are empty seats in the schedule.
            This should also test that a POST request can't be made to a schedule in full capacity.
        """
        response = self.client.get(self.url)
        
        # the schedule has not registrations, 
        # so the join button should be in the HTML
        self.assertContains(response, 'value="Join"')

        # add registrations to fill the schedule
        for i in range(self.schedule.course.max_students):
            # first create a student to register to the scheduled class
            student_fullname = "student-%i" % i
            student_email    = "%i@email.com" % i
            student = Person(fullname=student_fullname, email=student_email, slug=student_fullname)
            student.save()
            student.branch.add(self.branch)
            
            # then create the registration itself
            registration = Registration(schedule=self.schedule, student=student)
            registration.save()

        # visit the page again
        response = self.client.get(self.url)

        # the schedule should be full, 
        # so the join button should NOT be in the HTML
        self.assertNotContains(response, 'value="Join"')            
    
    
    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()