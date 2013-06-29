from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.conf import settings
from datetime import *
import shutil, os, os.path
from tradeschool.models import *
from tradeschool.utils import daterange



class ScheduleTestCase(TestCase):
    """ Tests the process of submitting a schedule using the frontend form.
    """
    fixtures = ['test_data.json', 'test_timerange.json', 'test_admin.json']
    
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
        
        # admin user for the branch
        self.password = 'testts123!'
        self.admin = User.objects.create_superuser('test_admin', 'tester@tradeschool.coop', self.password)
        self.admin.branch_set.add(self.branch)
        self.admin.save()
        
        self.url = reverse('schedule-add', kwargs={'branch_slug' : self.branch.slug })
        
        self.time = Time.objects.filter(venue__isnull=True)[0]
        
        self.new_teacher_data = {
                'teacher-fullname'  : 'new test teacher', 
                'teacher-bio'       : 'biobiobio', 
                'teacher-website'   : 'http://website.com', 
                'teacher-email'     : 'email@email.com', 
                'teacher-phone'     : '123-123-1234',
            }
        self.new_course_data = {
                'course-title'        : 'new test course', 
                'course-description'  : 'this is the description', 
                'course-max_students' : '20', 
            }
        self.time_data = {
                'time-time'             : self.time.pk
            } 
        self.barter_items_data = {
                'item-0-title'          : 'test item 01',
                'item-1-title'          : 'test item 02',
                'item-2-title'          : 'test item 03',
                'item-3-title'          : 'test item 04',
                'item-4-title'          : 'test item 05',
                'item-TOTAL_FORMS'      : 5,
                'item-INITIAL_FORMS'    : 0,
                'item-MAX_NUM_FORMS'    : 1000,                
            }
        self.empty_data = {
                'item-TOTAL_FORMS'      : 0,
                'item-INITIAL_FORMS'    : 0,
                'item-MAX_NUM_FORMS'    : 1000,
            }
        
        # merge the items of course, teacher, and barter item data
        self.valid_data = dict(self.new_course_data.items() + self.new_teacher_data.items() + self.barter_items_data.items() + self.time_data.items())
        

    def compare_schedule_to_data(self, schedule_obj):
        """ Asserts that the objects that were created after a successful schedule submission
            match the data that was used in the forms.
        """
        self.assertEqual(schedule_obj.course.title, self.valid_data['course-title'])
        self.assertEqual(schedule_obj.course.description, self.valid_data['course-description']) 
        self.assertEqual(schedule_obj.course.max_students, int(self.valid_data['course-max_students']))
        self.assertEqual(schedule_obj.start_time, self.time.start_time)
        self.assertEqual(schedule_obj.end_time, self.time.end_time)
        self.assertEqual(schedule_obj.venue, self.time.venue)        
        self.assertEqual(schedule_obj.course.teacher.fullname, self.valid_data['teacher-fullname'])
        self.assertEqual(schedule_obj.course.teacher.bio, self.valid_data['teacher-bio'])
        self.assertEqual(schedule_obj.course.teacher.email, self.valid_data['teacher-email'])
        self.assertEqual(schedule_obj.course.teacher.phone, self.valid_data['teacher-phone'])
        for item in schedule_obj.barteritem_set.all():
            self.assertTrue(item.title in self.valid_data.values())            

    
    def verify_timezone(self, saved_datetime_obj, saved_time):
        """ Verifies that a time was saved in a tz-aware way according to the branch's timeezone.
        """
        # verify branch's timezone
        current_tz = timezone.get_current_timezone()
        utc = pytz.timezone('UTC')
        self.assertEqual(current_tz.zone, self.branch.timezone)

        # do manual timezone conversion to the submitted date
        # start with localizing the non-aware dates to the branch's timezone
        localized_time = current_tz.localize(saved_datetime_obj)
        
        # verify that the dates now have the branch's tzinfo
        self.assertEqual(localized_time.tzinfo.zone, self.branch.timezone)
      
        # normalize dates to utc for storing in the database
        normalized_time = utc.normalize(localized_time.astimezone(utc))
        
        # verify that the normalized dates are the ones that were saved in the db
        self.assertEqual(normalized_time, saved_time)
                

    def test_timeslot_creation(self):
        """ Tests that time slots can be created from the admin backend,
            that they are stored and displayed with the branch's timezone,
            and that they are displayed in the schedule-submit view.
        """
        # login to admin
        self.client.login(username=self.admin.username, password=self.password)     

        # admin time add view
        url = reverse('admin:tradeschool_time_add')
        
        # these will become not-tz-aware strings, but they should be converted
        # to the branch's timezone 
        start_time = datetime(2030, 02, 02, 10, 0, 0)
        end_time   = datetime(2030, 02, 02, 12, 30, 0)
        
        # save a new time object
        data = {
                'start_time_0' : start_time.strftime('%Y-%m-%d'),
                'start_time_1' : start_time.strftime('%H:%M:%S'),
                'end_time_0'   : end_time.strftime('%Y-%m-%d'),
                'end_time_1'   : end_time.strftime('%H:%M:%S'),
                'venue'        : Venue.objects.filter(branch=self.branch)[0].pk,
                'branch'       : self.branch.pk,
            }
        
        response = self.client.post(url, data=data, follow=True)
        
        # verify the form was submitted successfully
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed('admin/change_form.html')        
        
        # saved time
        time = Time.objects.latest('created')

        # verify date and time were saved in a tz-aware way, normalized to UTC
        self.verify_timezone(start_time, time.start_time)
        self.verify_timezone(end_time, time.end_time)
        
        # verify that the timeslot appears on the schedule-submit form
        url = reverse('schedule-add', kwargs={ 'branch_slug' : self.branch.slug })
        response = self.client.get(url)
        self.assertContains(response, time.pk)
        
        
    def test_timerange_creation(self):
        """ Tests that a TimeRange saved in the admin backend results in the correct
            number of Time objects with data as it was set in the TimeRange form.
        """
        # login to admin
        self.client.login(username=self.admin.username, password=self.password)     

        # admin time add view
        url = reverse('admin:tradeschool_timerange_add')
        
        # these will become not-tz-aware strings, but they should be converted        
        # to the branch's timezone 
        start_time = datetime(2030, 02, 02, 10, 0, 0)
        end_time   = datetime(2030, 04, 02, 12, 30, 0)
        
        # save a new time object
        data = {
                'start_time' : start_time.strftime('%H:%M:%S'),
                'start_date' : start_time.strftime('%Y-%m-%d'),
                'end_time'   : end_time.strftime('%H:%M:%S'),
                'end_date'   : end_time.strftime('%Y-%m-%d'),
                'monday'     : 1,
                'branch'     : self.branch.pk,
            }
        
        response = self.client.post(url, data=data, follow=True)

        # verify the form was submitted successfully
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed('admin/change_form.html')        
        
        # saved timerange
        timerange = TimeRange.objects.latest('created')
        
        # saved time slots
        start_time  = datetime.combine(timerange.start_date, timerange.start_time)
        end_time    = datetime.combine(timerange.end_date, timerange.end_time)
        times = Time.objects.filter(start_time__gte=start_time, end_time__lte=end_time)
        
        # verify times were saved
        self.assertTrue(times.count > 4)
        

    def test_view_loading(self):
        """ Tests that the schedule-add view loads properly.
            If there's a branch-specific template file, make sure it's loaded as well.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_add.html')


    def test_empty_submission(self):
        """ Tests that submitting an empty form results in the expected error messages.
        """        
        response = self.client.post(self.url, data=self.empty_data)

        # an empty form should return 8 errors for the required fields
        self.assertContains(response, 'Please', count=8)
        
        # the same template should be rendered
        self.assertTemplateUsed(self.branch.slug + '/schedule_submit.html')


    def is_successful_submission(self, data):
        """ Tests that the submission of a schedule with valid data works.
        """
        # post the data to the schedule submission form
        response = self.client.post(self.url, data=data, follow=True)
        
        self.assertRedirects(response, response.redirect_chain[0][0], response.redirect_chain[0][1])
        self.assertTemplateUsed(self.branch.slug + '/schedule_submitted.html')

        # check that the schedule got saved correctly
        self.compare_schedule_to_data(response.context['schedule'])
        
        return response
        
    def test_schedule_submission_new_teacher_new_course(self):
        """ Tests the submission of a schedule of a new class by a new teacher.
        """
        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the schedule got saved correctly
        self.compare_schedule_to_data(response.context['schedule'])
        
        
    def test_schedule_submission_existing_teacher_new_course(self):
        """ Tests the submission of a schedule of a new class by an existing teacher.
        """
        # get a Person who teaches in the branch
        existing_teacher = Teacher.objects.filter(branch=self.branch)[0]

        # use the existing teacher's email for the form submission
        # when the teacher-email matches an existing objects,
        # the schedule should be saved to the existing teacher object
        self.valid_data['teacher-email'] = existing_teacher.email
        
        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the schedule got saved correctly
        self.compare_schedule_to_data(response.context['schedule'])


    def test_schedule_submission_existing_teacher_existing_course(self):
        """ Tests the submission of a schedule of an existing class by an existing teacher.
        """
        # get a Person who teaches in the branch
        existing_teacher = Teacher.objects.filter(branch=self.branch)[0]

        # use the existing teacher's email for the form submission
        # when the teacher-email matches an existing Person object,
        # the schedule should be saved to the existing Person object
        self.valid_data['teacher-email'] = existing_teacher.email

        # get an existing course in the branch
        existing_course = Course.objects.filter(branch=self.branch)[0]

        # use the existing course's title for the form submission
        # when the course-title matches an existing Course object,
        # the schedule should be saved to the existing Course object
        self.valid_data['course-title'] = existing_course.title
        
        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the schedule got saved correctly
        self.compare_schedule_to_data(response.context['schedule'])


    def test_venue_is_saved(self):
        """ Tests a successful submission with a Time object that has 
            a Venue foreignkey.
        """
        # save a time-venue relationship
        self.time.venue = Venue.objects.filter(branch=self.branch)[0]
        self.time.save()
        
        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the schedule got saved correctly
        self.compare_schedule_to_data(response.context['schedule'])


    def test_time_is_saved(self):
        """ Tests that the selected time in the form is saved in
            a tz-aware way in the database.
        """
        # get Time object
        time = Time.objects.get(pk=self.time_data['time-time'])

        # post the data to the schedule submission form
        response = self.client.post(self.url, data=self.valid_data, follow=True)

        # the saved schedule
        schedule = Schedule.objects.latest('created')
        
        # verify the Schedule times match the Time's times
        self.assertEqual(schedule.start_time, time.start_time)
        self.assertEqual(schedule.end_time, time.end_time)


    def test_time_deleted_after_successful_submission(self):
        """ Tests that the selected Time object gets deleted 
            after a schedule has been submitted successfully.
        """
        # get Time object
        time = Time.objects.get(pk=self.time_data['time-time'])
                
        # post the data to the schedule submission form
        response = self.client.post(self.url, data=self.valid_data, follow=True)

        # check that the time object got deleted 
        self.assertFalse(Time.objects.filter(pk=time.pk).exists())

    
    def test_schedule_emails_are_generated(self):
        """ Tests that a ScheduleEmailContainer is created after a successful schedule submission,
            and that 7 emails are copied to it from the BranchEmailContainer.
        """
        # submit a schedule
        response = self.is_successful_submission(self.valid_data)

        schedule = response.context['schedule']        
        
        # check that one ScheduleEmailContainer was created for the schedule
        self.assertEqual(ScheduleEmailContainer.objects.filter(schedule=schedule).count(), 1)

        # check that the ScheduleEmailContainer has all 7 Email objects
        self.assertEqual(schedule.emails.emails.__len__(), 7)
        
        # store this object in a variable for convenience 
        bec = BranchEmailContainer.objects.filter(branch__in=schedule.course.branch.all())[0]
                
        # iterate over the emails in the schedule's ScheduleEmailContainer
        for email_name, schedule_email_obj in schedule.emails.emails.items():
            # find the same email type in the BranchEmailContainer, 
            # where the schedule emails were copied from
            default_email = getattr(bec, email_name)

            # verify that the email was copied correctly
            self.assertEqual(schedule_email_obj.subject, default_email.subject)
            self.assertEqual(schedule_email_obj.content, default_email.content)        
        
    
    def test_teacher_confirmation_email(self):
        """ Tests that the TeacherConfirmation is sent after
            a successful submission.
        """
        # submit a schedule
        response = self.is_successful_submission(self.valid_data)        
        
        schedule = response.context['schedule']
        
        # test that one message was sent.
        self.assertEqual(len(mail.outbox), 1)        

        # verify the email status was updated
        email = schedule.emails.teacher_confirmation        
        self.assertEqual(email.email_status, 'sent')
        
        # verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, email.subject)


    def test_teacher_approval_email(self):
        """ Tests that the TeacherClassApproval is sent after a schedule is approved.
        """
        # submit a schedule
        response = self.is_successful_submission(self.valid_data)        
        
        schedule = response.context['schedule']
        url = reverse('schedule-list', kwargs={'branch_slug' : self.branch.slug, })        
        
        # empty the test outbox
        mail.outbox = []
                
        # approve the schedule
        schedule.course_status = 3 
        schedule.save()
        
        # test that one message was sent.
        self.assertEqual(len(mail.outbox), 1)        

        # verify the email status was updated
        email = schedule.emails.teacher_class_approval
        self.assertEqual(email.email_status, 'sent')            
        
        # verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, email.subject)
                
        
    def test_edit_schedule_template(self):
        """ Test that the schedule-edit view doesn't load unless 
            a schedule_slug for an existing Schedule object is provided.
        """
        # try to load the schedule-edit view without a schedule slug
        response = self.client.get(reverse('schedule-edit', kwargs={'branch_slug':self.branch.slug, 'schedule_slug':None}))
        
        # this should lead to a 404 page
        self.assertEqual(response.status_code, 404)
        
        # post a valid schedule data to save a new schedule
        response = self.client.post(self.url, data=self.valid_data, follow=True)
        
        # try loading the schedule-edit view for the saved schedule
        response = self.client.get(reverse('schedule-edit', kwargs={'branch_slug':self.branch.slug, 'schedule_slug':response.context['schedule'].slug }))
        
        # check that the correct template was loaded sucessfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_edit.html')
        
        
    def test_editing_schedule_with_empty_data(self):
        """ Test that editting an existing Schedule and submitting an empty
            form results in the expected number of errors.
        """
        # post a valid schedule data to save a new schedule
        response = self.client.post(self.url, data=self.valid_data, follow=True)
        
        schedule = response.context['schedule']
        schedule_edit_url = reverse('schedule-edit', kwargs={'branch_slug':self.branch.slug, 'schedule_slug':schedule.slug })
        
        # post empty data to the form
        response = self.client.post(schedule_edit_url, data=self.empty_data)
        
        # an empty form should return 7 errors for the required fields
        # there's one less error when editing a schedule sine the time 
        # is already saved and can't be edited in the form
        self.assertContains(response, 'Please', count=7)


    def test_editing_schedule_with_valid_data(self):
        """ Test that editting an existing Schedule and submitting edited
            fields results in the new data being saved correctly.
            This includes any new BarterItem objects that may have been added
            to the form.
        """        
        # post a valid schedule data to save a new schedule
        response = self.client.post(self.url, data=self.valid_data, follow=True)

        schedule = response.context['schedule']
        schedule_edit_url = reverse('schedule-edit', kwargs={'branch_slug':self.branch.slug, 'schedule_slug':schedule.slug })
    
        # make some changes to the data
        for key, value in self.new_teacher_data.items():
            self.valid_data[key] = "1%s" % value
        for key, value in self.new_course_data.items():
            self.valid_data[key] = "1%s" % value
        
        # edit a barter item 
        self.barter_items_data['item-0-title'] = 'edited item'
        
        # add a barter item
        self.barter_items_data['item-5-title'] = 'new barter item'
        
        # update the barter item formset number
        self.barter_items_data['item-TOTAL_FORMS'] = 6
        
        # combine all dictionaries
        self.valid_data = dict(self.new_teacher_data.items() + self.new_course_data.items() + self.barter_items_data.items() + self.time_data.items())
        
        # post edited data to the form
        response = self.client.post(schedule_edit_url, data=self.valid_data, follow=True)

        # check that the schedule got saved correctly
        self.compare_schedule_to_data(response.context['schedule'])


    def test_schedule_status(self):
        """ Tests that the only approved schedules appear on the schedule-list view.
        """
        # submit a schedule
        response = self.is_successful_submission(self.valid_data)        

        schedule = response.context['schedule']
        url = reverse('schedule-list', kwargs={'branch_slug' : self.branch.slug, })

        # go to schedule-list view
        response = self.client.get(url)

        # verify that the schedule is not on the page
        self.assertNotContains(response, schedule.course.title)

        # approve the schedule
        schedule.course_status = 3 
        schedule.save()

        # reload the page
        response = self.client.get(url)

        # verify that the schedule appears on the page
        self.assertContains(response, schedule.course.title)


    def test_schedule_past_page(self):
        """ Tests that the schedule-past page loads and displays
            only approved scheduled classes that took place in the branch.
        """
        # submit a schedule
        response = self.is_successful_submission(self.valid_data)
        schedule = response.context['schedule']
        branch   = schedule.course.branch.all()[0]
        
        # there should be no past schedules at this point, 
        # so the link to past scheduled should not appear 
        # on the branch's schedule-list view
        schedule_list_url = reverse('schedule-list', kwargs={'branch_slug' : branch.slug })
        response = self.client.get(schedule_list_url)
        #self.assertNotContains(response, 'Past') ** NOTE: not implemented yet -Or
        
        # past schedules url
        url = reverse('schedule-list-past', kwargs={'branch_slug' : branch.slug })
        
        # verify page loads with the branch's template
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/schedule_list_past.html')
        
        # verify the scheduled class is not in there
        self.assertNotContains(response, schedule.course.title)
                
        # move schedule to a past time
        now = datetime.utcnow().replace(tzinfo=utc) 
        schedule.start_time = now - timedelta(hours=47)
        schedule.end_time   = now - timedelta(hours=48)
        schedule.course_status = 0
        schedule.save()
        
        # schedule should still not appear, since it's approved
        response = self.client.get(url) 
        self.assertNotContains(response, schedule.course.title)
        
        # change the scheduled class's status to approved
        schedule.course_status = 3
        schedule.save()

        # verify that the scheduled class now appears 
        response = self.client.get(url) 
        self.assertContains(response, schedule.course.title)
        

    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()

        # clear cache
        cache.clear()