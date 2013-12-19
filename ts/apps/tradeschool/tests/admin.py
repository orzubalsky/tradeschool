from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from datetime import *
from tradeschool.models import *


class AdminTestCase(TestCase):
    """
    Tests the process of submitting feedback
    for a schedule using the frontend form.
    """
    fixtures = ['email_initial_data.json',
                'teacher-info.json',
                'sample_data.json'
                ]

    def setUp(self):
        """ Create a Site and branch for testing.
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'

        self.site = Site.objects.all()[0]

        self.password = 'testts123!'
        self.admin = Person.objects.create_superuser(
            username='test_admin',
            fullname="test admin",
            email='tester@tradeschool.coop',
            password=self.password
        )

        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()
        self.branch.organizers.add(self.admin)

    def login(self):
        self.client.login(username=self.admin.username, password=self.password)

    def test_admin_login(self):
        """Test that logging in as an admin works."""

        branch_add_url = '/admin/tradeschool/branch/add/'
        # go to page without logging in, be redirected to the login page
        response = self.client.get(branch_add_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/login.html')

        # login and try again, this time it should work
        self.login()

        response = self.client.get(branch_add_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/change_form.html')

    def test_logged_in_user_language(self):
        """
        Test that settings the language field for the logged in Person
        translates the admin backend to the selected language.
        """
        self.login()

        language = 'es_mx'
        url = reverse('admin:tradeschool_organizer_add')

        # save language in user
        self.admin.language = language
        self.admin.save()

        # it's not possible to use translation.activate
        # in the context of a unittest-
        # what happens is that once a get/post request is made,
        # django calls translation.activate with the language that's
        # defined in settings (or the testcase's settings override).
        # This means we can't really test the language switching
        # unless we override the settings.
        settings.LANGUAGE_CODE = language

        # load a page to check the language setting
        response = self.client.get(url)

        # verify the languages match. test in 2 parts,
        # since the language codes don't really match-
        # they're both es_es and es-es.
        self.assertEqual(
            self.admin.language[:2],
            response.context['LANGUAGE_CODE'][:2]
        )

        self.assertEqual(
            self.admin.language[3:],
            response.context['LANGUAGE_CODE'][3:]
        )

    def tearDown(self):
        """
        Delete branch files in case something went wrong
        and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()
