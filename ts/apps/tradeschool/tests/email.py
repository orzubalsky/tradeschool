from django.test import TestCase
from django.core.management import call_command
from django.contrib.sites.models import Site
from django.conf import settings
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from tradeschool.models import *


class EmailTestCase(TestCase):
    """
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
        self.course = Course.objects.filter(branch=self.branch)[0]
        self.course.status = 'approved'
        self.course.save()

    def do_registration(self, registration_count=1):
        """ Register to a given course n times.
        """
        for i in range(registration_count):
            # first create a student to register to the scheduled class
            student_fullname = "student-%i" % i
            student_email = "%i@email.com" % i
            student = Person.objects.create_user(
                fullname=student_fullname,
                email=student_email,
                slug=student_fullname
            )
            student.branches.add(self.branch)

            # then create the registration itself
            registration = Registration(
                course=self.course,
                student=student
            )
            registration.save()

            # add an item to the registration
            registration.items.add(self.course.barteritem_set.all()[0])

    def set_time_for_automatic_email_sending(self, email_obj):
        """
        Sets the datetime fields on both the Course and the email_obj
        to be within the range that the send_timed_emails management command
        filters by.
        """
        # edit the Course time to be within the range
        # that the mangagement command is filtering by
        # at the moment it is set to 14 days before and after
        self.course.start_time = timezone.now() + timedelta(days=1)
        self.course.end_time = timezone.now() + timedelta(days=1, minutes=60)
        self.course.save()

        # edit the Email object to be set to be sent in the last hour
        email_obj.send_on = timezone.now() - timedelta(minutes=15)
        email_obj.save()

        # verify the Email hasn't been sent and that it will be
        # processed by the management command
        self.assertEqual(email_obj.email_status, 'not_sent')

    def verify_email_data(self, message_obj, email_obj, registration=None):
        """ Compares the data from the email message in the mail outbox
            and the Email object.
        """
        self.assertEqual(
            message_obj.extra_headers['Reply-To'],
            self.branch.email
        )
        self.assertEqual(message_obj.subject, email_obj.subject)
        self.assertEqual(
            message_obj.body,
            email_obj.preview(self.course, registration)
        )

    def verify_email_teacher(self, email_obj):
        """ Tests that the an Email is sent to a teacher
            with the correct data.
        """
        # verify the email is in the outbox
        self.assertEqual(len(mail.outbox), 1)

        # verify the email data is correct
        sent_email = mail.outbox[0]
        self.verify_email_data(sent_email, email_obj)
        self.assertTrue(self.course.teacher.email in sent_email.to)

    def verify_email_students(self, email_obj, registration_count=5):
        """ Tests that an Email is sent to students with
            the correct data to all registered students.
        """
        # verify the email is in the outbox
        self.assertEqual(len(mail.outbox), registration_count)

        # verify the email data is correct
        for i in range(registration_count):
            sent_email = mail.outbox[i]

            registration = self.course.registration_set.all()[i]

            self.verify_email_data(sent_email, email_obj, registration)

            if registration.registration_status == 'registered':
                self.assertTrue(registration.student.email in sent_email.to)

    def test_teacher_reminder(self):
        """ Tests the TeacherReminder Email."""
        automatic_email = self.course.teacherreminder

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email data
        self.verify_email_teacher(automatic_email)

    def test_teacher_feedback(self):
        """ Tests the TeacherFeedback Email."""
        automatic_email = self.course.teacherfeedback

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email data
        self.verify_email_teacher(automatic_email)

    def test_student_reminder(self):
        """ Tests the StudentReminder Email."""
        automatic_email = self.course.studentreminder

        # register multiple times to the course
        self.do_registration(5)

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email is in the outbox
        registration_count = Registration.objects.filter(
            course=self.course,
            registration_status='registered').count()
        self.verify_email_students(automatic_email, registration_count)

    def test_student_feedback(self):
        """ Tests the StudentFeedback Email."""

        automatic_email = self.course.studentfeedback

        # register multiple times to the course
        self.do_registration(5)

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email is in the outbox
        registration_count = Registration.objects.filter(
            course=self.course, registration_status='registered').count()
        self.verify_email_students(automatic_email, registration_count)

    def tearDown(self):
        """ Delete branch files in case something went wrong
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()
