from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from datetime import *
import shutil, os, os.path
from tradeschool.models import *



class ScheduleSubmissionTestCase(TestCase):
    """ Tests the process of submitting a schedule using the frontend form.
    """
    fixtures = ['test_data.json', 'test_timerange.json']
    
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

        self.url = reverse('schedule-add', kwargs={'branch_slug' : self.branch.slug })
        
        self.new_teacher_data = {
                'teacher-fullname'  : 'new test teahcer', 
                'teacher-bio'       : 'biobiobio', 
                'teacher-website'   : 'http://website.com', 
                'teacher-email'     : 'email@email.com', 
                'teacher-phone'     : '123-123-1234',
            }
        self.new_course_data = {
                'course-title'        : 'new test course', 
                'course-description'  : 'this is the description', 
                'course-max_students' : '20', 
            }
        self.time_data = {
                'time-time'             : ''
            } 
        self.barter_items_data = {
                'item-TOTAL_FORMS'      : 5,
                'item-INITIAL_FORMS'    : 0,
                'item-MAX_NUM_FORMS'    : 1000,
                'item-0-title'          : 'test item 01',
                'item-0-requested'      : '1',
                'item-1-title'          : 'test item 02',
                'item-1-requested'      : '1',
                'item-2-title'          : 'test item 03',
                'item-2-requested'      : '1',
                'item-3-title'          : 'test item 04',
                'item-3-requested'      : '1',
                'item-4-title'          : 'test item 05',
                'item-4-requested'      : '1',                                                                
            }
        self.empty_data = {
                'item-TOTAL_FORMS'      : 0,
                'item-INITIAL_FORMS'    : 0,
                'item-MAX_NUM_FORMS'    : 1000,
            }

    def test_view_loading(self):
        """ Tests that the schedule-add view loads properly.
            If there's a branch-specific template file, make sure it's loaded as well.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_add.html')


    def test_empty_submission(self):
        """ Tests that submitting an empty form results in the expected error messages.
        """        
        response = self.client.post(self.url, data=self.empty_data)

        # an empty form should return 8 errors for the required fields
        self.assertContains(response, 'Please', count=8)


    def test_schedule_submission(self):
        """ Tests the submission of a schedule of a new class by a new teacher.
        """
        # merge the items of course, teacher, and barter item data
        data = dict(self.new_course_data.items() + self.new_teacher_data.items() + self.barter_items_data.items() + self.time_data.items())
        
        # post the data to the schedule submission form
        response = self.client.post(self.url, data=data)
        
        print response.templates[0].name


    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()