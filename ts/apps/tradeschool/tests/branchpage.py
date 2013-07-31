from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import translation
from datetime import *
import shutil, os, os.path
from tradeschool.utils import Bunch
from tradeschool.models import *



class BranchPageTestCase(TestCase):
    """ 
    """
    fixtures = ['email_initial_data.json', 
                'teacher-info.json', 
                'test_admin.json', 
                'test_branch.json',
                ]    
    
    def setUp(self):
        """ Create a Site and an admin User for testing.
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'
                
        self.site   = Site(domain='http://test.tradeschool.coop', name='test site', id=2)
        self.site.save()
        
        self.password = 'testts123!'
        self.admin = Person.objects.create_superuser(username='test_admin', fullname='test admin', email='tester@tradeschool.coop', password=self.password)
        
        self.branch = Branch.objects.all()[0]
        self.branch_page_data = {
            'branch'  : self.branch,
            'url'     : '/test-page/',
            'title'   : 'test page',
            'content' : 'test page content',
            }
        self.branch_page = BranchPage(
            branch      = self.branch_page_data['branch'],
            url         = self.branch_page_data['url'],
            title       = self.branch_page_data['title'],
            content     = self.branch_page_data['content'],
            )
        self.url = reverse('branch-page', kwargs={'branch_slug' : self.branch.slug, 'url' : self.branch_page.url })
                

    def test_page_creation(self):
        """ Tests that creating a BranchPage results in the page displaying on the website.
        """
        # save a new BranchPage
        self.branch_page.save()

        # go to the new page's url
        response = self.client.get(self.url)

        # verify the page is loading 
        self.assertEqual(response.status_code, 200)        
        
        # verify that the BranchPage data is correct
        self.assertContains(response, self.branch_page_data['title'])
        self.assertContains(response, self.branch_page_data['content'])
        
    
    def test_is_active_false(self):
        """
        """
        # change the page's status to inactive
        # inactive pages should stay in the db but not on the website
        self.branch_page.is_active = False
        self.branch_page.save()

        # verify the page is not loading
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
    

    def test_is_active_true(self):
        """
        """
        # change the page's status to active
        self.branch_page.is_active = True
        self.branch_page.save()

        # verify the page is loading
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


    def test_is_visible_false(self):
        """
        """
        # change the page to not visible (not in navigation)
        self.branch_page.is_active = True        
        self.branch_page.is_visible = False
        self.branch_page.save()

        # verify the page is not on the navigation menu
        response = self.client.get(reverse('schedule-list', kwargs={'branch_slug' : self.branch.slug, }))
        self.assertNotContains(response, self.branch_page.url)
        

    def test_is_visible_true(self):
        """
        """
        # change the page to not visible (not in navigation)
        self.branch_page.is_active = True        
        self.branch_page.is_visible = True
        self.branch_page.save()

        response = self.client.get(reverse('schedule-list', kwargs={'branch_slug' : self.branch.slug, }))
        self.assertContains(response, self.branch_page.url)        
        
        
    def test_deletion(self):
        """
        """
        # save branch page
        self.branch_page.save()
        
        # delete the page
        self.branch_page.delete()
          
        # verify the page is gone
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
    

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