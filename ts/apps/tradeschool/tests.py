"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from datetime import *
import shutil, os, os.path
from tradeschool.models import *



class BranchSetupTestCase(TestCase):
    """Test the process of setting up a new branch."""
    
    def setUp(self):
        """Create a Site and an admin User for testing."""
        
        
        self.site   = Site(domain='http://test.tradeschool.coop', name='test site', id=2)
        self.site.save()
        
        self.password = 'testts123!'
        self.admin = User.objects.create_superuser('test_admin', 'tester@tradeschool.coop', self.password)
        
        self.branch_add_url = '/admin/tradeschool/branch/add/'
        self.branch_data = {
                'title'                   : 'test branch', 
                'city'                    : 'test city', 
                'country'                 : 'US', 
                'slug'                    : 'test-branch', 
                'email'                   : 'test@tradeschool.coop', 
                'timezone'                : 'America/New_York',
                'language'                : 'en',
                'site'                    : self.site.pk,
                'header_copy'             : 'header',
                'intro_copy'              : 'intro text',
                'footer_copy'             : 'footer text',
                'organizers'              : self.admin.pk,
                'emails-TOTAL_FORMS'      : 0,
                'emails-INITIAL_FORMS'    : 0,
                'emails-MAX_NUM_FORMS'    : 1,
                'photo_set-TOTAL_FORMS'   : 0,
                'photo_set-INITIAL_FORMS' : 0,
                'photo_set-MAX_NUM_FORMS' : 1000,
            }
        self.empty_form = {
                'emails-TOTAL_FORMS'      : 0,
                'emails-INITIAL_FORMS'    : 0,
                'emails-MAX_NUM_FORMS'    : 1,
                'photo_set-TOTAL_FORMS'   : 0,
                'photo_set-INITIAL_FORMS' : 0,
                'photo_set-MAX_NUM_FORMS' : 1000,
            }
        
    def test_admin_login(self):
        """Test that logging in as an admin works."""
        
        # go to page without logging in, be redirected to the login page
        response = self.client.get(self.branch_add_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/login.html')
        
        # login and try again, this time it should work
        self.client.login(username=self.admin.username, password=self.password)        

        response = self.client.get(self.branch_add_url)

        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed('admin/change_form.html')


    def test_branch_creation(self):
        """Test valid and invalid branch form submission from admin."""
        
        self.client.login(username=self.admin.username, password=self.password)

        # submit an empty form
        response = self.client.post(self.branch_add_url, data=self.empty_form)

        # check that the same template is displayed (form + errors)
        self.assertTemplateUsed('admin/change_form.html')
        
        # an empty form should return 12 errors for the required fields
        self.assertContains(response, 'This field is required', count=12)
        
        # now submit valid form
        response = self.client.post(self.branch_add_url, follow=True, data=self.branch_data)
        
        # check that the branch was created successfully, following a redirect
        self.assertRedirects(response, response.redirect_chain[0][0], response.redirect_chain[0][1])
        self.assertTemplateUsed('admin/change_list.html')
        self.assertEqual(response.status_code, 200)

        # store branch in a variable
        self.branch = Branch.objects.get(slug=self.branch_data['slug'])   
        
        # check that one BranchEmailContainer was created for branch
        self.assertEqual(BranchEmailContainer.objects.filter(branch=self.branch).count(), 1)
        
        # check that the BranchEmailContainer has all 7 Email objects
        self.assertEqual(self.branch.emails.emails.__len__(), 7)
        
        # check that all branch templates and files were created
        branch_files_dir = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.branch.slug)
        
        default_files_count = len([f for f in os.listdir(settings.DEFAULT_BRANCH_TEMPLATE_DIR) if os.path.isfile(os.path.join(settings.DEFAULT_BRANCH_TEMPLATE_DIR, f))])
        branch_files_count = len([f for f in os.listdir(branch_files_dir) if os.path.isfile(os.path.join(branch_files_dir, f))])

        self.assertEqual(default_files_count, branch_files_count)
        
        # Delete files that were created in the process of creating a branch.
        self.branch.delete_files()
        

        def tearDown(self):
            """Delete branch files in case something went wrong and the files weren't deleted."""

            directory = os.path.join(settings.BRANCH_TEMPLATE_DIR, 'test-branch')

            if os.path.exists(directory):
                shutil.rmtree(directory)
                

"""
class RegistrationTestCase(TestCase):
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
        response = self.client.get(reverse('schedule-register', kwargs={ 'schedule_slug': self.schedule.slug }))        
        print response
        self.assertEqual(1 + 1, 2)
"""