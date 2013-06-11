from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.conf import settings
from datetime import *
import shutil, os, os.path
from tradeschool.models import *



class ScheduleSubmissionTestCase(TestCase):
    """ Tests the process of submitting a schedule using the frontend form.
    """
    fixtures = ['test_data.json', 'test_timerange.json']
    
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
        
        self.url = reverse('schedule-add', kwargs={'branch_slug' : self.branch.slug })
        
        self.time = Time.objects.filter(venue__isnull=True)[0]
        
        self.new_teacher_data = {
                'teacher-fullname'  : 'new test teahcer', 
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
        for item in schedule_obj.items.all():
            self.assertTrue(item.title in self.valid_data.values())            


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
        
                

    def tearDown(self):
        """ Delete branch files in case something went wrong 
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()