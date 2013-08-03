from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.sites.models import Site
from django.forms.models import model_to_dict
from django.conf import settings
from django.core import mail
from django.utils import timezone
from datetime import datetime, timedelta
import os.path
from tradeschool.models import *



class EmailTestCase(TestCase):
    """ 
    """
    fixtures = ['email_initial_data.json', 
                'teacher-info.json', 
                'test_data.json', 
                'test_course.json',
                'test_schedule.json', 
                'test_person.json'
                ]
    
    def setUp(self):
        """ Create a Site and branch for testing.
        """
        # test in english so we count html strings correctly
        settings.LANGUAGE_CODE = 'en'
        
        self.site   = Site.objects.all()[0]
        
        # change the language to english for language-based assertations
        self.branch = Branch.objects.all()[0]
        self.branch.language = 'en'
        self.branch.save()
        
        # use this schedule for testing
        self.schedule = Schedule.objects.filter(course__branches=self.branch)[0]
        self.schedule.course_status = 3
        self.schedule.save()


    def do_registration(self, registration_count=1):
        """ Register to a given schedule n times.
        """
        for i in range(registration_count):
            # first create a student to register to the scheduled class
            student_fullname = "student-%i" % i
            student_email    = "%i@email.com" % i
            student = Person.objects.create_user(fullname=student_fullname, email=student_email, slug=student_fullname)
            student.save()
            student.branches.add(self.branch)

            # then create the registration itself
            registration = Registration(schedule=self.schedule, student=student)
            registration.save()
            
            # add an item to the registration
            registration.items.add(self.schedule.barteritem_set.all()[0])
            registration.save()


    def set_time_for_automatic_email_sending(self, email_obj):
        """ 
        Sets the datetime fields on both the Schedule and the email_obj
        to be within the range that the send_timed_emails management command
        filters by.
        """
        # edit the Schedule time to be within the range
        # that the mangagement command is filtering by
        # at the moment it is set to 14 days before and after
        self.schedule.start_time = timezone.now() + timedelta(days=1)
        self.schedule.end_time = timezone.now() + timedelta(days=1, minutes=60)
        self.schedule.save()

        # edit the Email object to be set to be sent in the last hour
        email_obj.send_on = timezone.now() - timedelta(minutes=15)
        email_obj.save()

        # verify the Email hasn't been sent and that it will be
        # processed by the management command
        self.assertEqual(email_obj.email_status, 'not_sent')


    def verify_email_data(self, message_obj, email_obj):
        """ Compares the data from the email message in the mail outbox
            and the Email object.
        """
        self.assertEqual(message_obj.from_email, self.branch.email)
        self.assertEqual(message_obj.subject, email_obj.subject)
        self.assertEqual(message_obj.body, email_obj.preview(self.schedule))        


    def verify_email_teacher(self, email_obj):
        """ Tests that the an Email is sent to a teacher 
            with the correct data.
        """
        # verify the email is in the outbox
        self.assertEqual(len(mail.outbox), 1)
        
        # verify the email data is correct
        sent_email = mail.outbox[0]
        self.verify_email_data(sent_email, email_obj)
        self.assertTrue(self.schedule.course.teacher.email in sent_email.to)


    def verify_email_students(self, email_obj, registration_count = 5):
        """ Tests that an Email is sent to students with 
            the correct data to all registered students.
        """        
        # verify the email is in the outbox
        self.assertEqual(len(mail.outbox), registration_count)

        # verify the email data is correct
        for i in range(registration_count):
            sent_email = mail.outbox[i]
            self.verify_email_data(sent_email, email_obj)
            self.assertTrue(self.schedule.students.all()[i].email in sent_email.to)


    def test_teacher_reminder(self):
        """ Tests the TeacherReminder Email."""
        automatic_email = self.schedule.emails.teacher_reminder

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email data
        self.verify_email_teacher(automatic_email)


    def test_teacher_feedback(self):
        """ Tests the TeacherFeedback Email."""        
        automatic_email = self.schedule.emails.teacher_feedback

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email data
        self.verify_email_teacher(automatic_email)   


    def test_student_reminder(self):
        """ Tests the StudentReminder Email."""        
        automatic_email = self.schedule.emails.student_reminder

        # register multiple times to the schedule
        self.do_registration(5)

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email is in the outbox
        self.verify_email_students(automatic_email, self.schedule.registration_set.count())


    def test_student_feedback(self):
        """ Tests the StudentFeedback Email."""        
        
        automatic_email = self.schedule.emails.student_feedback

        # register multiple times to the schedule
        self.do_registration(5)

        self.set_time_for_automatic_email_sending(automatic_email)

        # call the management command
        call_command('send_timed_emails')

        # verify the email is in the outbox
        self.verify_email_students(automatic_email, self.schedule.registration_set.count())


    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()