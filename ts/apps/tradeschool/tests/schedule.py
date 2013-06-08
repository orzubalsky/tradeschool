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
    fixtures = ['test_data.json']
    
    def setUp(self):
        """ Create a Site and branch for testing.
        """
        self.site   = Site.objects.all()[0]
        self.branch = Branch.objects.all()[0]
        self.venue  = Venue.objects.filter(branch=self.branch)[0]
        self.course = Course.objects.filter(branch=self.branch)[0]
        

    def test_test(self):
        print self.site
        print self.branch
        print self.venue
        print self.course
        

    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()