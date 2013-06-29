from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
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
        for registered_item in registration_obj.items.all():
            self.assertEqual(registered_item.pk, int(self.valid_data['item-items'][0]))


    def do_register(self):
        """ Register to a given schedule.
        """
        item = self.schedule.barteritem_set.all()[0]
        self.valid_data['item-items'] = [ item.pk, ]
        
        # post a valid form
        response = self.client.post(self.url, data=self.valid_data, follow=True)
        
        return response
                
        
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
        response = self.do_register()
        
        self.assertTemplateUsed(self.branch.slug + '/schedule_registered.html')

        # check that the registration got saved correctly
        self.compare_registration_to_data(response.context['registration'])
        
    
    def test_student_confirmation_email(self):
        """ Tests that the StudentConfirmation is sent after a schedule is approved.
        """
        # register to a schedule
        response = self.do_register()
        
        # test that one message was sent.
        self.assertEqual(len(mail.outbox), 1)        

        email = self.schedule.emails.student_confirmation        
        self.assertEqual(email.email_status, 'sent')
        
        # verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, email.subject)        
        
        
    def test_register_again(self):
        """ Tests that a student who is already registered to a scheduled class
            can't register to it again.
        """
        # register
        response = self.do_register()

        # register again
        response = self.do_register()
        
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


    def test_unregistration(self):
        """ Tests that the schedule-unregister view loads with the 
            correct template, that unregistering changes the status in
            the Registration object, and that it is not possible to
            unregister more than once.
        """
        # register
        response = self.do_register()
        
        registration = response.context['registration']
        
        # construct unregister url from branch, schedule, and saved registration
        url = reverse('schedule-unregister', kwargs={'branch_slug' : self.branch.slug, 'schedule_slug' : self.schedule.slug, 'student_slug' : registration.student.slug })        

        # go to the url
        response = self.client.get(url)
        
        # check that the correct template is loading
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_register.html')
        
        # unregister
        response = self.client.post(url, data={}, follow=True)
        
        # check that the page was redirected
        self.assertRedirects(response, response.redirect_chain[0][0], response.redirect_chain[0][1])
        self.assertTemplateUsed(self.branch.slug + '/schedule_list.html')
        
        # get registration again after it was saved in the view function
        registration = Registration.objects.get(pk=registration.pk)
        
        # check that the registration status was changed
        self.assertEqual(registration.registration_status, 'unregistered')
        
        # try unregistering again
        response = self.client.get(url)
        
        # make sure it's not possible
        self.assertContains(response, 'already unregistered')


    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()




class RegistrationSeleniumTestCase(LiveServerTestCase):
    """
    """
    fixtures = ['test_data.json', 'test_schedule.json']


    @classmethod
    def setUpClass(self):
        """ Start Selenium.
        """
        # start Firefox websdriver
        self.selenium = WebDriver()

        # call super setup method
        super(RegistrationSeleniumTestCase, self).setUpClass()


    def setUp(self):
        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()  

        # approve a scheduled class so it appears on the website
        self.schedule = Schedule.objects.filter(course__branch=self.branch)[0]
        self.schedule.course_status = 3
        self.schedule.save()
        
        self.timeout = 2


    def test_registration_toggle_button(self):
        """ Tests that clicking the title of a scheduled class
            on the website expands the div.
        """
        # construct server url
        schedule_list_url = reverse('schedule-list', kwargs={ 'branch_slug' : self.branch.slug })
        live_url = "%s%s" % (self.live_server_url, schedule_list_url)

        # load page
        self.selenium.get(live_url)

        # find a scheduled class title and click on it
        toggle_button = self.selenium.find_element_by_class_name('toggle')        
        
        self.assertTrue(toggle_button.is_displayed())
        toggle_button.click()
        
        
    def test_registration_join_button(self):
        """ Tests that clicking on the join button sends an ajax request.
        """
        # construct server url
        schedule_register_url = reverse('schedule-register', kwargs={ 'branch_slug' : self.branch.slug, 'schedule_slug' : self.schedule.slug })
        live_url = "%s%s" % (self.live_server_url, schedule_register_url)

        # load page
        self.selenium.get(live_url)

        # find a scheduled class join button
        join_button = self.selenium.find_element_by_class_name('join')        
        
        self.assertTrue(join_button.is_displayed())

        join_button.click()        


    def tearDown(self):
        """ Delete Branch files.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()        

    @classmethod
    def tearDownClass(self):
        # stop selenium    
        self.selenium.quit()

        # call super teardown method
        super(RegistrationSeleniumTestCase, self).tearDownClass()