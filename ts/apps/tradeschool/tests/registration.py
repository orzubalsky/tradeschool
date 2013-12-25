from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from datetime import *
from tradeschool.models import *


class RegistrationTestCase(TestCase):
    """
    Tests the process of registering and unregistering
    to a course using the frontend forms.
    """
    fixtures = ['email_initial_data.json',
                'teacher-info.json',
                'sample_data.json'
                ]

    def setUp(self):
        """
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'

        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()

        self.course = Course.objects.filter(branch=self.branch)[0]

        self.valid_data = {
            'student-fullname': 'test student',
            'student-email': 'test123!@email.com',
            'student-phone': '',
        }
        self.url = reverse('course-register', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': self.course.slug
        })

    def compare_registration_to_data(self, registration_obj):
        """ Asserts that the objects that were created after a successful
            registration submission match the data that was used in the forms.
        """
        self.assertEqual(registration_obj.course, self.course)
        self.assertEqual(
            registration_obj.student.fullname,
            self.valid_data['student-fullname']
        )
        self.assertEqual(registration_obj.registration_status, 'registered')
        self.assertTrue(self.branch in registration_obj.student.branches.all())
        for registered_item in registration_obj.items.all():
            self.assertEqual(
                registered_item.pk,
                int(self.valid_data['item-items'][0])
            )

    def do_register(self):
        """ Register to a given course.
        """
        item = self.course.barteritem_set.all()[0]
        self.valid_data['item-items'] = [item.pk, ]

        # post a valid form
        response = self.client.post(
            self.url, data=self.valid_data, follow=True)

        return response

    def test_view_is_loading(self):
        """
        Tests that the course-register view loads with the correct template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/course_register.html')

    def test_registration_empty_form(self):
        """
        Test that an empty submitted registration form returns the expected
        number of errors, for fullname, email, and at least one checked item.
        """
        data = {}

        # post an empty form
        response = self.client.post(self.url, data=data, follow=True)

        # an empty form should return 3 errors for the required fields
        self.assertContains(response, 'Please', count=3)

    def test_registration_valid_form(self):
        """
        Tests that a submission of valid data
        results in a successful registration.
        """
        response = self.do_register()

        self.assertTemplateUsed(self.branch.slug + '/course_registered.html')
        #print response.context
        # check that the registration got saved correctly
        self.compare_registration_to_data(response.context['registration'])

    def test_student_confirmation_email(self):
        """
        Tests that the StudentConfirmation is sent
        after a course is approved.
        """
        # register to a course
        self.do_register()

        # test that one message was sent.
        self.assertEqual(len(mail.outbox), 1)

        email = self.course.studentconfirmation
        #self.assertEqual(email.email_status, 'sent')

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
        self.assertTemplateUsed(self.branch.slug + '/course_registered.html')

        # check that the error message is in the page
        self.assertContains(
            response, 'You are already registered to this class')

    def test_capacity(self):
        """
        Tests that the Join button is only visible
        if there are empty seats in the course.
        This should also test that a POST request
        can't be made to a course in full capacity.
        """
        response = self.client.get(self.url)

        # the course has not registrations,
        # so the join button should be in the HTML
        self.assertContains(response, 'value="Join"')

        # add registrations to fill the course
        for i in range(self.course.max_students):
            # first create a student to register to the scheduled class
            student_fullname = "student-%i" % i
            student_email = "%i@email.com" % i
            student = Person.objects.create_user(
                fullname=student_fullname,
                email=student_email,
                slug=student_fullname
            )
            student.save()
            student.branches.add(self.branch)

            # then create the registration itself
            registration = Registration(
                course=self.course,
                student=student
            )
            registration.save()

        # visit the page again
        response = self.client.get(self.url)

        # the course should be full,
        # so the join button should NOT be in the HTML
        self.assertNotContains(response, 'value="Join"')

    def test_unregistration(self):
        """
        Tests that the course-unregister view loads with the
        correct template, that unregistering changes the status in
        the Registration object, and that it is not possible to
        unregister more than once.
        """
        # register
        response = self.do_register()

        registration = response.context['registration']

        # construct unregister url from branch, course,
        # and saved registration
        url = reverse('course-unregister', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': self.course.slug,
            'student_slug': registration.student.slug
        })

        # go to the url
        response = self.client.get(url)

        # check that the correct template is loading
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/course_register.html')

        # unregister
        response = self.client.post(url, data={}, follow=True)

        # check that the page was redirected
        self.assertRedirects(
            response,
            response.redirect_chain[0][0],
            response.redirect_chain[0][1]
        )
        self.assertTemplateUsed(self.branch.slug + '/course_list.html')

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
