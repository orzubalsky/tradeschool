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



class FeedbackTestCase(TestCase):
    """ Tests the process of submitting feedback for a schedule using the frontend form.
    """
    fixtures = ['test_data.json', 'test_schedule.json']
    
    def setUp(self):
        """ Create a Site and branch for testing.
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'
        
        self.site   = Site.objects.all()[0]
        
        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()
        
        # use this schedule for testing
        self.schedule = Schedule.objects.filter(course__branch=self.branch)[0]
        self.schedule.course_status = 3
        self.schedule.save()
        
        self.future_start_time = self.schedule.start_time
        self.future_end_time = self.schedule.end_time        

        self.move_schedule_to_past()
        
        # construct feedback url
        self.url = reverse('schedule-feedback', kwargs={'branch_slug' : self.branch.slug, 'schedule_slug' : self.schedule.slug, 'feedback_type' : 'student' })        


    def move_schedule_to_past(self):
        """ Sets the schedule time fields to past times."""
        now = datetime.utcnow().replace(tzinfo=utc) 
        self.schedule.start_time = now - timedelta(hours=47)
        self.schedule.end_time = now - timedelta(hours=48)
        self.schedule.save()
        
        
    def move_schedule_to_future(self):
        """ Sets the schedule time fields to future times."""        
        now = datetime.utcnow().replace(tzinfo=utc) 
        self.schedule.start_time = self.future_start_time
        self.schedule.end_time = self.future_end_time
        self.schedule.save()         


    def test_view_loading(self):
        """ Tests that the schedule-feedbacj view loads properly.
            If there's a branch-specific template file, make sure it's loaded as well.
        """
        # approve schedule and save
        self.schedule.course_status = 0
        self.schedule.save()
                
        # make sure schedule is 'pending' and that 
        # the scheduled class did not happen yet
        self.assertEqual(self.schedule.course_status, 0)
        self.move_schedule_to_future()
        
        # load url
        response = self.client.get(self.url)
        
        # page should not load if the schedule is not approved
        self.assertEqual(response.status_code, 404)
        
        # approve schedule and save
        self.schedule.course_status = 3
        self.schedule.save()
        
        # loading the url again
        response = self.client.get(self.url)

        # if scheduled class didn't take place yet, the page should not load
        self.assertEqual(response.status_code, 404)
        
        # move the schedule to a time in the past
        self.move_schedule_to_past()
        
        # loading the url again
        response = self.client.get(self.url)
        
        # view should load now
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_feedback.html')
    

    def test_empty_submission(self):
        """ Tests that submitting an empty form results in the expected error messages.
        """        
        # test an empty form submission
        response = self.client.post(self.url, data={}, follow=True)
        
        # an empty form should return 1 error for the required fields
        self.assertContains(response, 'Please', count=1)
        

    def test_valid_submission(self):
        """ Tests that that valid feedback data is submitted and saved correctly.
        """
        response = self.client.post(self.url, data={'content' : 'test feedback' }, follow=True)
        
        # check the form was submitted successfully
        self.assertRedirects(response, response.redirect_chain[0][0], response.redirect_chain[0][1])
        self.assertTemplateUsed(self.branch.slug + '/schedule_list.html')
        self.assertEqual(self.schedule.feedback_set.count(), 1)

            
    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()