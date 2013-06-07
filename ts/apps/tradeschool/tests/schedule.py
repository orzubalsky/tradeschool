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
    def setUp(self):
        """ Create a Site and branch for testing.
        """
        self.site   = Site(domain='http://test.tradeschool.coop', name='test site', id=2)
        self.site.save()

        self.branch = Branch(
                title       = 'test branch',
                city        = 'test city', 
                country     = 'US', 
                slug        = 'test-branch', 
                email       = 'test@tradeschool.coop', 
                timezone    = 'America/New_York',
                language    = 'en',
                site        = self.site,
                header_copy = 'header',
                intro_copy  = 'intro text',
                footer_copy = 'footer text',
            )
        self.branch.save()
        
        self.venue = Venue()