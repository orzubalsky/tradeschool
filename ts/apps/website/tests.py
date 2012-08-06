"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from tradeschool.models import *
from django.core.files.storage import default_storage as storage
import os, sys

class BranchTestCase(unittest.TestCase):
    def setUp(self):
        self.test_branch = Branch.objects.create(title="test branch", slug="test-los-angeles", city="Los Angeles", state="CA", country="US", email="test@testing.com", timezone="America/Los_Angeles", phone="")
       
    def test_branch_files_are_created(self):
        """Branch files should be created in /static/branches/{slug}/{file} """
        for filename in self.test_branch.files():
            self.assertTrue(storage.exists(self.test_branch.folder() + filename))

    def test_branch_files_are_deleted(self):
        """Branch files should be removed when the model is deleted """
        files = self.test_branch.files()
        folder = self.test_branch.folder()
        self.test_branch.delete()       
        for filename in files:
            self.assertFalse(storage.exists(folder + filename))
        self.assertFalse(os.path.exists(folder))
            