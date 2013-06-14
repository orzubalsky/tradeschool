from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.conf import settings
from django.core import mail
from datetime import *
import shutil, os, os.path
from tradeschool.models import *



class EmailTestCase(TestCase):
    """ 
    """
    fixtures = ['test_data.json', 'test_schedule.json', 'test_person.json']
    
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
        self.schedule = Schedule.objects.filter(course__branch=self.branch)[0]
        self.schedule.course_status = 3
        self.schedule.save()


    def do_registration(self, registration_count=1):
        """ Register to a given schedule n times.
        """
        for i in range(registration_count):
            # first create a student to register to the scheduled class
            student_fullname = "student-%i" % i
            student_email    = "%i@email.com" % i
            student = Person(fullname=student_fullname, email=student_email, slug=student_fullname)
            student.save()
            student.branch.add(self.branch)

            # then create the registration itself
            registration = Registration(schedule=self.schedule, student=student)
            registration.save()
            
            # add an item to the registration
            registered_item = RegisteredItem(barter_item=self.schedule.items.all()[0])
            registration.registereditem_set.add(registered_item)
            registration.save()


    def verify_email_data(self, message_obj, email_obj):
        """ Compares the data from the email message in the mail outbox
            and the Email object.
        """
        self.assertEqual(message_obj.from_email, self.branch.email)
        self.assertEqual(message_obj.subject, email_obj.subject)
        self.assertEqual(message_obj.body, email_obj.preview(self.schedule))        


    def test_email_teacher_reminder(self):
        """ Tests that the TeacherReminder Email is sent with 
            the correct data.
        """
        # send email via the ScheduleEmailContainer object
        sec = self.schedule.emails
        
        # send email
        sec.email_teacher(sec.teacher_reminder)
        
        # verify the email is in the outbox
        self.assertEqual(len(mail.outbox), 1)
        
        # verify the email data is correct
        sent_email = mail.outbox[0]
        self.verify_email_data(sent_email, sec.teacher_reminder)
        self.assertTrue(self.schedule.course.teacher.email in sent_email.to)


    def test_email_student_reminders(self):
        """ Tests that the StudentReminder Email is sent with 
            the correct data to all registered students.
        """
        registration_count = 5
        
        # register multiple times to the schedule
        self.do_registration(registration_count)
        
        # send email via the ScheduleEmailContainer object
        sec = self.schedule.emails

        # send emails
        sec.email_students(sec.student_reminder)

        # verify the email is in the outbox
        self.assertEqual(len(mail.outbox), registration_count)

        # verify the email data is correct
        for i in range(registration_count):
            sent_email = mail.outbox[i]
            self.verify_email_data(sent_email, sec.student_reminder)
            self.assertTrue(self.schedule.students.all()[i].email in sent_email.to) 
        

    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()