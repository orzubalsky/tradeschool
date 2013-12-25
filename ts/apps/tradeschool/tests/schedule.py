from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from datetime import *
from tradeschool.models import *


class CourseTestCase(TestCase):
    """ Tests the process of submitting a course using the frontend form.
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

        # admin user for the branch
        self.password = 'testts123!'
        self.admin = Person.objects.create_superuser(
            username='test_admin',
            email='tester@tradeschool.coop',
            fullname='test admin',
            password=self.password
        )
        self.admin.branches.add(self.branch)
        self.branch.organizers.add(self.admin)
        self.admin.save()

        self.url = reverse(
            'course-add', kwargs={'branch_slug': self.branch.slug})

        self.time = Time.objects.filter(venue__isnull=True)[0]

        self.new_teacher_data = {
            'teacher-fullname': 'new test teacher',
            'teacher-bio': 'biobiobio',
            'teacher-website': 'http://website.com',
            'teacher-email': 'email@email.com',
            'teacher-phone': '123-123-1234',
        }
        self.new_course_data = {
            'course-title': 'new test course',
            'course-description': 'this is the description',
            'course-max_students': '20',
        }
        self.time_data = {
            'time-time': self.time.pk
        }
        self.barter_items_data = {
            'item-0-title': 'test item 01',
            'item-1-title': 'test item 02',
            'item-2-title': 'test item 03',
            'item-3-title': 'test item 04',
            'item-4-title': 'test item 05',
            'item-TOTAL_FORMS': 5,
            'item-INITIAL_FORMS': 0,
            'item-MAX_NUM_FORMS': 1000,
        }
        self.empty_data = {
            'item-TOTAL_FORMS': 0,
            'item-INITIAL_FORMS': 0,
            'item-MAX_NUM_FORMS': 1000,
        }

        # merge the items of course, teacher, and barter item data
        self.valid_data = dict(
            self.new_course_data.items()
            + self.new_teacher_data.items()
            + self.barter_items_data.items()
            + self.time_data.items()
        )

    def compare_course_to_data(self, course_obj):
        """
        Asserts that the objects that were created after
        a successful course submission match
        the data that was used in the forms.
        """
        self.assertEqual(
            course_obj.title,
            self.valid_data['course-title']
        )
        self.assertEqual(
            course_obj.description,
            self.valid_data['course-description']
        )
        self.assertEqual(
            course_obj.max_students,
            int(self.valid_data['course-max_students'])
        )
        self.assertEqual(
            course_obj.start_time,
            self.time.start_time
        )
        self.assertEqual(
            course_obj.end_time,
            self.time.end_time
        )
        if self.time.venue is None:
            self.assertEqual(
                course_obj.venue,
                self.branch.venue_set.all()[0]
            )
        else:
            self.assertEqual(
                course_obj.venue,
                self.time.venue
            )
        self.assertEqual(
            course_obj.teacher.fullname,
            self.valid_data['teacher-fullname']
        )
        self.assertEqual(
            course_obj.teacher.bio,
            self.valid_data['teacher-bio']
        )
        self.assertEqual(
            course_obj.teacher.email,
            self.valid_data['teacher-email']
        )
        self.assertEqual(
            course_obj.teacher.phone,
            self.valid_data['teacher-phone']
        )
        self.assertTrue(course_obj.slug.__len__() > 0)
        self.assertTrue(course_obj.teacher.slug.__len__() > 0)
        for item in course_obj.barteritem_set.all():
            self.assertTrue(item.title in self.valid_data.values())

    def verify_timezone(self, saved_datetime_obj, saved_time):
        """
        Verifies that a time was saved in a tz-aware way
        according to the branch's timeezone.
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

        # verify that the normalized dates are
        # the ones that were saved in the db
        self.assertEqual(normalized_time, saved_time)

    def test_timeslot_creation(self):
        """ Tests that time slots can be created from the admin backend,
            that they are stored and displayed with the branch's timezone,
            and that they are displayed in the course-submit view.
        """
        # login to admin
        self.client.login(username=self.admin.username, password=self.password)

        # admin time add view
        url = reverse('admin:tradeschool_time_add')

        # these will become not-tz-aware strings, but they should be converted
        # to the branch's timezone
        start_time = datetime(2030, 02, 02, 10, 0, 0)
        end_time = datetime(2030, 02, 02, 12, 30, 0)

        # save a new time object
        data = {
            'start_time_0': start_time.strftime('%Y-%m-%d'),
            'start_time_1': start_time.strftime('%H:%M:%S'),
            'end_time_0': end_time.strftime('%Y-%m-%d'),
            'end_time_1': end_time.strftime('%H:%M:%S'),
            'venue': Venue.objects.filter(branch=self.branch)[0].pk,
            'branch': self.branch.pk,
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

        # verify that the timeslot appears on the course-submit form
        url = reverse('course-add', kwargs={'branch_slug': self.branch.slug})
        response = self.client.get(url)
        self.assertContains(response, time.pk)

    def test_timerange_creation(self):
        """
        Tests that a TimeRange saved in the admin backend
        results in the correct number of Time objects
        with data as it was set in the TimeRange form.
        """
        # timerange count
        previous_timerange_count = TimeRange.objects.all().count()

        # login to admin
        self.client.login(username=self.admin.username, password=self.password)

        # admin time add view
        url = reverse('admin:tradeschool_timerange_add')

        # these will become not-tz-aware strings,
        # but they should be converted to the branch's timezone
        start_time = timezone.make_aware(
            datetime(2030, 02, 02, 10, 0, 0), timezone.utc)

        end_time = timezone.make_aware(
            datetime(2030, 04, 02, 12, 30, 0), timezone.utc)

        # save a new timerange object
        data = {
            'start_time': start_time.strftime('%H:%M:%S'),
            'start_date': start_time.strftime('%Y-%m-%d'),
            'end_time': end_time.strftime('%H:%M:%S'),
            'end_date': end_time.strftime('%Y-%m-%d'),
            'monday': 'on',
            'branch': self.branch.pk,
        }

        response = self.client.post(url, data=data, follow=True)

        # verify the form was submitted successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/change_form.html')

        # verify a new timerange was saved
        current_timerange_count = TimeRange.objects.all().count()
        self.assertEqual(
            (previous_timerange_count + 1),
            current_timerange_count
        )

        # saved timerange
        timerange = TimeRange.objects.latest('created')

        # saved time slots
        start_time = datetime.combine(
            timerange.start_date, timerange.start_time)

        end_time = datetime.combine(
            timerange.end_date, timerange.end_time)

        times = Time.objects.filter(
            start_time__gte=start_time,
            end_time__lte=end_time
        )

        # verify times were saved
        self.assertTrue(times.count > 4)

        # verify venue not saved
        for i, time in enumerate(times):
            self.assertEqual(times[i].venue, None)

    def test_timerange_creation_with_venue(self):
        """
        Tests that a TimeRange saved in the admin backend
        results in the correct number of Time objects
        with data as it was set in the TimeRange form,
        including the venue.
        """
        # timerange count
        previous_timerange_count = TimeRange.objects.all().count()

        # login to admin
        self.client.login(
            username=self.admin.username,
            password=self.password
        )

        # admin time add view
        url = reverse('admin:tradeschool_timerange_add')

        # these will become not-tz-aware strings, but they should be converted
        # to the branch's timezone
        start_time = timezone.make_aware(
            datetime(2030, 02, 02, 10, 0, 0), timezone.utc)

        end_time = timezone.make_aware(
            datetime(2030, 04, 02, 12, 30, 0), timezone.utc)

        # save a new timerange object
        data = {
            'start_time': start_time.strftime('%H:%M:%S'),
            'start_date': start_time.strftime('%Y-%m-%d'),
            'end_time': end_time.strftime('%H:%M:%S'),
            'end_date': end_time.strftime('%Y-%m-%d'),
            'monday': 'on',
            'branch': self.branch.pk,
            'venue': self.branch.venue_set.all()[0].pk
        }

        response = self.client.post(url, data=data, follow=True)

        # verify a new timerange was saved
        current_timerange_count = TimeRange.objects.all().count()
        self.assertEqual(
            (previous_timerange_count + 1),
            current_timerange_count
        )

        # saved timerange
        timerange = TimeRange.objects.latest('created')

        # saved time slots
        start_time = datetime.combine(
            timerange.start_date, timerange.start_time)

        end_time = datetime.combine(
            timerange.end_date, timerange.end_time)

        times = Time.objects.filter(
            start_time__gte=start_time,
            end_time__lte=end_time
        )

        # verify times were saved
        self.assertTrue(times.count > 4)

        # verify venue not saved
        for i, time in enumerate(times):
            self.assertEqual(times[i].venue, self.branch.venue_set.all()[0])

    def test_view_loading(self):
        """
        Tests that the course-add view loads properly.
        If there's a branch-specific template file,
        make sure it's loaded as well.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/course_add.html')

    def test_empty_submission(self):
        """
        Tests that submitting an empty form
        results in the expected error messages.
        """
        response = self.client.post(self.url, data=self.empty_data)

        # an empty form should return 8 errors for the required fields
        self.assertContains(response, 'Please', count=8)

        # the same template should be rendered
        self.assertTemplateUsed(self.branch.slug + '/course_submit.html')

    def is_successful_submission(self, data):
        """ Tests that the submission of a course with valid data works.
        """
        # post the data to the course submission form
        response = self.client.post(self.url, data=data, follow=True)

        self.assertRedirects(
            response,
            response.redirect_chain[0][0],
            response.redirect_chain[0][1]
        )
        self.assertTemplateUsed(self.branch.slug + '/course_submitted.html')

        # check that the course got saved correctly
        self.compare_course_to_data(response.context['course'])

        return response

    def test_course_submission_new_teacher_new_course(self):
        """ Tests the submission of a course of a new class by a new teacher.
        """
        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the course got saved correctly
        self.compare_course_to_data(response.context['course'])

    def test_course_submission_existing_teacher_new_course(self):
        """
        Tests the submission of a course of a new class
        by an existing teacher.
        """
        # get a Person who teaches in the branch
        existing_teacher = Teacher.objects.filter(branches=self.branch)[0]

        # use the existing teacher's email for the form submission
        # when the teacher-email matches an existing objects,
        # the course should be saved to the existing teacher object
        self.valid_data['teacher-email'] = existing_teacher.email

        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the course got saved correctly
        self.compare_course_to_data(response.context['course'])

    # def test_course_submission_existing_teacher_existing_course(self):
    #     """
    #     Tests the submission of a course of an existing class
    #     by an existing teacher.
    #     """
    #     # get a Person who teaches in the branch
    #     existing_teacher = Teacher.objects.filter(branches=self.branch)[0]

    #     # use the existing teacher's email for the form submission
    #     # when the teacher-email matches an existing Person object,
    #     # the course should be saved to the existing Person object
    #     self.valid_data['teacher-email'] = existing_teacher.email

    #     # get an existing course in the branch
    #     existing_course = Course.objects.filter(branch=self.branch)[0]

    #     # use the existing course's title for the form submission
    #     # when the course-title matches an existing Course object,
    #     # the course should be saved to the existing Course object
    #     self.valid_data['course-title'] = existing_course.title

    #     # test that the form submission worked
    #     response = self.is_successful_submission(self.valid_data)

    #     # check that the course got saved correctly
    #     self.compare_course_to_data(response.context['course'])

    def test_venue_is_saved(self):
        """
        Tests a successful submission with a Time object that has
        a Venue foreignkey.
        """
        # save a time-venue relationship
        self.time.venue = Venue.objects.filter(branch=self.branch)[0]
        self.time.save()

        # test that the form submission worked
        response = self.is_successful_submission(self.valid_data)

        # check that the course got saved correctly
        self.compare_course_to_data(response.context['course'])

    def test_time_is_saved(self):
        """ Tests that the selected time in the form is saved in
            a tz-aware way in the database.
        """
        # get Time object
        time = Time.objects.get(pk=self.time_data['time-time'])

        # post the data to the course submission form
        response = self.client.post(
            self.url, data=self.valid_data, follow=True)

        # the saved course
        course = Course.objects.latest('created')

        # verify the Course times match the Time's times
        self.assertEqual(course.start_time, time.start_time)
        self.assertEqual(course.end_time, time.end_time)

    def test_time_deleted_after_successful_submission(self):
        """
        Tests that the selected Time object gets deleted
        after a course has been submitted successfully.
        """
        # get Time object
        time = Time.objects.get(pk=self.time_data['time-time'])

        # post the data to the course submission form
        response = self.client.post(
            self.url, data=self.valid_data, follow=True)

        # check that the time object got deleted
        self.assertFalse(Time.objects.filter(pk=time.pk).exists())

    def test_course_emails_are_generated(self):
        """
        Tests that a CourseEmailContainer is created
        after a successful course submission,
        and that 7 emails are copied to it from the BranchEmailContainer.
        """
        # submit a course
        response = self.is_successful_submission(self.valid_data)

        course = response.context['course']

        # check that the CourseEmailContainer has all 7 Email objects
        self.assertEqual(course.emails.__len__(), 7)

        # iterate over the emails in the course's CourseEmailContainer
        for email_name, course_email_obj in course.emails.items():
            # find the same email type in the BranchEmailContainer,
            # where the course emails were copied from
            default_email = getattr(course.branch, email_name)

            # verify that the email was copied correctly
            self.assertEqual(course_email_obj.subject, default_email.subject)
            self.assertEqual(course_email_obj.content, default_email.content)

    def test_teacher_confirmation_email(self):
        """ Tests that the TeacherConfirmation is sent after
            a successful submission.
        """
        # submit a course
        response = self.is_successful_submission(self.valid_data)

        course = response.context['course']

        # test that one message was sent.
        self.assertEqual(len(mail.outbox), 1)

        # verify the email status was updated
        email = course.teacherconfirmation
        self.assertEqual(email.email_status, 'sent')

        # verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, email.subject)

    def test_teacher_approval_email(self):
        """
        Tests that the TeacherClassApproval is sent
        after a course is approved.
        """
        # submit a course
        response = self.is_successful_submission(self.valid_data)

        course = response.context['course']

        # empty the test outbox
        mail.outbox = []

        # approve the course
        course.status = 'approved'
        course.save()

        # test that one message was sent.
        self.assertEqual(len(mail.outbox), 1)

        # verify the email status was updated
        email = course.teacherclassapproval
        self.assertEqual(email.email_status, 'sent')

        # verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, email.subject)

    def test_edit_course_template(self):
        """
        Test that the course-edit view doesn't load unless
        a course_slug for an existing Course object is provided.
        """
        # try to load the course-edit view without a course slug
        response = self.client.get(reverse('course-edit', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': None
        }))

        # this should lead to a 404 page
        self.assertEqual(response.status_code, 404)

        # post a valid course data to save a new course
        response = self.client.post(
            self.url, data=self.valid_data, follow=True)

        # try loading the course-edit view for the saved course
        response = self.client.get(reverse('course-edit', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': response.context['course'].slug
        }))

        # check that the correct template was loaded sucessfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/course_edit.html')

    def test_editing_course_with_empty_data(self):
        """ Test that editting an existing Course and submitting an empty
            form results in the expected number of errors.
        """
        # post a valid course data to save a new course
        response = self.client.post(
            self.url, data=self.valid_data, follow=True)

        course = response.context['course']
        course_edit_url = reverse('course-edit', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': course.slug
        })

        # post empty data to the form
        response = self.client.post(course_edit_url, data=self.empty_data)

        # an empty form should return 7 errors for the required fields
        # there's one less error when editing a course sine the time
        # is already saved and can't be edited in the form
        self.assertContains(response, 'Please', count=7)

    def test_editing_course_with_valid_data(self):
        """ Test that editting an existing Course and submitting edited
            fields results in the new data being saved correctly.
            This includes any new BarterItem objects that may have been added
            to the form.
        """
        # post a valid course data to save a new course
        response = self.client.post(
            self.url, data=self.valid_data, follow=True)

        course = response.context['course']
        course_edit_url = reverse('course-edit', kwargs={
            'branch_slug': self.branch.slug,
            'course_slug': course.slug
        })

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
        self.valid_data = dict(
            self.new_teacher_data.items()
            + self.new_course_data.items()
            + self.barter_items_data.items()
            + self.time_data.items()
        )

        # post edited data to the form
        response = self.client.post(
            course_edit_url, data=self.valid_data, follow=True)

        # check that the course got saved correctly
        self.compare_course_to_data(response.context['course'])

    def test_course_status(self):
        """
        Tests that the only approved courses appear on the course-list view
        """
        # submit a course
        response = self.is_successful_submission(self.valid_data)

        course = response.context['course']
        url = reverse(
            'course-list', kwargs={'branch_slug': self.branch.slug, })

        # go to course-list view
        response = self.client.get(url)

        # verify that the course is not on the page
        self.assertNotContains(response, course.title)

        # approve the course
        course.status = 'approved'
        course.save()

        # reload the page
        response = self.client.get(url)

        # verify that the course appears on the page
        self.assertContains(response, course.title)

    def test_course_past_page(self):
        """ Tests that the course-past page loads and displays
            only approved scheduled classes that took place in the branch.
        """
        # submit a course
        response = self.is_successful_submission(self.valid_data)
        course = response.context['course']
        branch = course.branch

        # there should be no past courses at this point,
        # so the link to past scheduled should not appear
        # on the branch's course-list view
        course_list_url = reverse(
            'course-list', kwargs={'branch_slug': branch.slug})
        response = self.client.get(course_list_url)
        #self.assertNotContains(response, 'Past') NOTE: not implemented yet -Or

        # past courses url
        url = reverse(
            'course-list-past', kwargs={'branch_slug': branch.slug})

        # verify page loads with the branch's template
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.branch.slug + '/course_list_past.html')

        # verify the scheduled class is not in there
        self.assertNotContains(response, course.title)

        # move course to a past time
        now = datetime.utcnow().replace(tzinfo=utc)
        course.start_time = now - timedelta(hours=47)
        course.end_time = now - timedelta(hours=48)
        course.status = 'pending'
        course.save()

        # course should still not appear, since it's approved
        response = self.client.get(url)
        self.assertNotContains(response, course.title)

        # change the scheduled class's status to approved
        course.status = 'approved'
        course.save()

        # verify that the scheduled class now appears
        response = self.client.get(url)
        self.assertContains(response, course.title)

    def tearDown(self):
        """ Delete branch files in case something went wrong
            and the files weren't deleted.
        """
        # delete branches' files
        for branch in Branch.objects.all():
            branch.delete_files()

        # clear cache
        cache.clear()
