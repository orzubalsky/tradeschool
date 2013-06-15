from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from datetime import *
import shutil, os, os.path
from tradeschool.utils import Bunch
from tradeschool.models import *



class BranchSetupTestCase(TestCase):
    """ Test the process of setting up a new branch.
    """
    fixtures = ['test_admin.json', 'test_branch.json']    
    
    def setUp(self):
        """ Create a Site and an admin User for testing.
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'
                
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
        self.branch = Branch(
                title       = self.branch_data['title'],
                city        = self.branch_data['city'],
                country     = self.branch_data['country'],
                slug        = self.branch_data['slug'],
                email       = self.branch_data['email'],
                timezone    = self.branch_data['timezone'],
                language    = self.branch_data['language'],
                site        = self.site,
                header_copy = self.branch_data['header_copy'],
                intro_copy  = self.branch_data['intro_copy'],
                footer_copy = self.branch_data['footer_copy'],                                
            )
        
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
        """ Test valid and invalid branch form submission from admin.
        """
        # Login
        self.client.login(username=self.admin.username, password=self.password)

        # submit an empty form
        response = self.client.post(self.branch_add_url, data=self.empty_form)

        # check that the same template is displayed (form + errors)
        self.assertTemplateUsed('admin/change_form.html')
        
        # an empty form should return 9 errors for the required fields
        self.assertContains(response, 'This field is required', count=9)
        
        # now submit valid form
        response = self.client.post(self.branch_add_url, follow=True, data=self.branch_data)
        
        # store branch in a variable
        branch = Branch.objects.get(slug=self.branch_data['slug'])
                
        # check that the branch was created successfully, following a redirect
        self.assertRedirects(response, response.redirect_chain[0][0], response.redirect_chain[0][1])
        self.assertTemplateUsed('admin/change_list.html')
        self.assertEqual(response.status_code, 200)


    def test_branch_emails(self):
        """ Test that copies of the email templates were created
            When a new branch is saved.
        """
        # save a new branch
        self.branch.save()

        # check that one BranchEmailContainer was created for branch
        self.assertEqual(BranchEmailContainer.objects.filter(branch=self.branch).count(), 1)

        # check that the BranchEmailContainer has all 7 Email objects
        self.assertEqual(self.branch.emails.emails.__len__(), 7)


    def test_branch_files(self):
        """ Test that the branch-specific files are 
            created properly when a new branch is saved.
        """
        # save a new branch
        self.branch.save()
        
        # check that all branch templates and files were created
        branch_files_dir = os.path.join(settings.BRANCH_TEMPLATE_DIR, self.branch.slug)
        
        default_files_count = len([f for f in os.listdir(settings.DEFAULT_BRANCH_TEMPLATE_DIR) if os.path.isfile(os.path.join(settings.DEFAULT_BRANCH_TEMPLATE_DIR, f))])
        branch_files_count = len([f for f in os.listdir(branch_files_dir) if os.path.isfile(os.path.join(branch_files_dir, f))])

        self.assertEqual(default_files_count, branch_files_count)
        
    
    def test_branch_on_homepage(self):
        """ Tests whether a new branch appears on the homepage.
        """
        # render the homepage
        response = self.client.get(reverse('branch-list'))
        
        # make sure the view loads with the correct template
        self.assertTemplateUsed('hub/branch_list.html')
        self.assertEqual(response.status_code, 200)
        
        # check that the branch is not there (sanity check)
        self.assertNotContains(response, self.branch_data['slug'])
        
        # save a new branch
        self.branch.save()
        
        # render the homepage again
        response = self.client.get(reverse('branch-list'))        
        
        # check that the branch is now there
        self.assertContains(response, self.branch_data['slug'])
        

    def test_branch_templates_loading(self):
        """ Tests whether the branch-specific template files
            are rendered in the various branch views.
        """
        # save a new branch
        self.branch.save()
        
        # schedule-list view
        response = self.client.get(reverse('schedule-list', kwargs={'branch_slug' : self.branch.slug, }))
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed(self.branch.slug + '/schedule_list.html')


    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        directory = os.path.join(settings.BRANCH_TEMPLATE_DIR, 'test-branch')

        if os.path.exists(directory):
            shutil.rmtree(directory)
            
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()            