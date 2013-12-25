from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from datetime import *
from tradeschool.models import *


class FeedbackTestCase(TestCase):
    """
    Tests the process of submitting feedback
    for a course using the frontend form.
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

        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()

        # use this course for testing
        self.course = ApprovedCourse.objects.filter(branch=self.branch)[0]
        self.course.status = 'approved'
        self.course.save()

        self.future_start_time = self.course.start_time
        self.future_end_time = self.course.end_time

        self.move_course_to_past()

        # construct feedback url
        self.url = reverse('course-feedback', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': self.course.slug,
            'feedback_type': 'student'
        })

    def move_course_to_past(self):
        """ Sets the course time fields to past times."""
        now = datetime.utcnow().replace(tzinfo=utc)
        self.course.start_time = now - timedelta(hours=47)
        self.course.end_time = now - timedelta(hours=48)
        self.course.save()

    def move_course_to_future(self):
        """ Sets the course time fields to future times."""
        self.course.start_time = self.future_start_time
        self.course.end_time = self.future_end_time
        self.course.save()

    def test_view_loading(self):
        """ Tests that the course-feedbacj view loads properly.
            If there's a branch-specific template file,
            make sure it's loaded as well.
        """
        # approve course and save
        self.course.status = 'pending'
        self.course.save()

        # make sure course is 'pending' and that
        # the scheduled class did not happen yet
        self.assertEqual(self.course.status, 'pending')
        self.move_course_to_future()

        # load url
        response = self.client.get(self.url)

        # page should not load if the course is not approved
        self.assertEqual(response.status_code, 404)

        # approve course and save
        self.course.status = 'approved'
        self.course.save()

        # loading the url again
        response = self.client.get(self.url)

        # if scheduled class didn't take place yet, the page should not load
        self.assertEqual(response.status_code, 404)

        # move the course to a time in the past
        self.move_course_to_past()

        # loading the url again
        response = self.client.get(self.url)

        # view should load now
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/course_feedback.html')

    def test_empty_submission(self):
        """
        Tests that submitting an empty form
        results in the expected error messages.
        """
        # test an empty form submission
        response = self.client.post(self.url, data={}, follow=True)

        # an empty form should return 1 error for the required fields
        self.assertContains(response, 'Please', count=1)

    def test_valid_submission(self):
        """
        Tests that that valid feedback data is submitted and saved correctly.
        """
        response = self.client.post(
            self.url,
            data={'content': 'test feedback'},
            follow=True
        )

        # check the form was submitted successfully
        self.assertRedirects(
            response,
            response.redirect_chain[0][0],
            response.redirect_chain[0][1]
        )
        self.assertTemplateUsed(self.branch.slug + '/course_list.html')
        self.assertEqual(self.course.feedback_set.count(), 1)

    def tearDown(self):
        """ Delete branch files in case something went wrong
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()
