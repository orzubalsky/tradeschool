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
        self.valid_data = {
                'student-fullname' : 'test student',
                'student-email'    : 'test123!@email.com',
                'student-phone'    : '',
            }
        self.url = reverse('schedule-register', kwargs={'branch_slug': self.branch.slug, 'schedule_slug': self.schedule.slug })


    def compare_registration_to_data(self, registration_obj):
        """ Asserts that the objects that were created after a successful 
            registration submission match the data that was used in the forms.
        """
        self.assertEqual(registration_obj.schedule, self.schedule)
        self.assertEqual(registration_obj.student.fullname, self.valid_data['student-fullname'])
        self.assertEqual(registration_obj.registration_status, 'registered')
        self.assertTrue(self.branch in registration_obj.student.branch.all())
        for registered_item in registration_obj.registereditem_set.all():
            self.assertEqual(registered_item.barter_item.pk, int(self.valid_data['item-items'][0]))
            self.assertEqual(registered_item.registered, 1)            


    def test_view_is_loading(self):
        """ Tests that the schedule-register view loads with the correct template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_register.html')


    def test_registration_empty_form(self):
        """ Test that an empty submitted registration form returns the expected
            number of errors, for fullname, email, and at least one checked item.
        """
        data = {}
        
        # post an empty form
        response = self.client.post(self.url, data=data, follow=True)
        
        # an empty form should return 3 errors for the required fields
        self.assertContains(response, 'Please', count=3)


    def test_registration_valid_form(self):
        """ Tests that a submission of valid data results in a successful registration.
        """
        item = self.schedule.items.all()[0]
        self.valid_data['item-items'] = [ item.pk, ]
        
        # post a valid form
        response = self.client.post(self.url, data=self.valid_data, follow=True)

        self.assertTemplateUsed(self.branch.slug + '/schedule_registered.html')

        # check that the registration got saved correctly
        self.compare_registration_to_data(response.context['registration'])
        
        
    def test_register_again(self):
        """ Tests that a student who is already registered to a scheduled class
            can't register to it again.
        """
        item = self.schedule.items.all()[0]
        self.valid_data['item-items'] = [ item.pk, ]

        # post a valid form
        response = self.client.post(self.url, data=self.valid_data, follow=True)

        # register again
        response = self.client.post(self.url, data=self.valid_data, follow=True)        
        
        # make sure the same template is used (didn't redirect)
        self.assertTemplateUsed(self.branch.slug + '/schedule_registered.html')        
        
        # check that the error message is in the page
        self.assertContains(response, 'You are already registered to this class')
                

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