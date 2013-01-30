# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StudentConfirmation'
        db.create_table('tradeschool_studentconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
        ))
        db.send_create_signal('tradeschool', ['StudentConfirmation'])

        # Adding model 'StudentReminder'
        db.create_table('tradeschool_studentreminder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal('tradeschool', ['StudentReminder'])

        # Adding model 'StudentFeedback'
        db.create_table('tradeschool_studentfeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal('tradeschool', ['StudentFeedback'])

        # Adding model 'TeacherConfirmation'
        db.create_table('tradeschool_teacherconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
        ))
        db.send_create_signal('tradeschool', ['TeacherConfirmation'])

        # Adding model 'TeacherClassApproval'
        db.create_table('tradeschool_teacherclassapproval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
        ))
        db.send_create_signal('tradeschool', ['TeacherClassApproval'])

        # Adding model 'TeacherReminder'
        db.create_table('tradeschool_teacherreminder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal('tradeschool', ['TeacherReminder'])

        # Adding model 'TeacherFeedback'
        db.create_table('tradeschool_teacherfeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal('tradeschool', ['TeacherFeedback'])

        # Adding model 'DefaultEmailContainer'
        db.create_table('tradeschool_defaultemailcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentConfirmation'])),
            ('student_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentReminder'])),
            ('student_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentFeedback'])),
            ('teacher_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherConfirmation'])),
            ('teacher_class_approval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherClassApproval'])),
            ('teacher_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherReminder'])),
            ('teacher_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherFeedback'])),
        ))
        db.send_create_signal('tradeschool', ['DefaultEmailContainer'])

        # Adding model 'BranchEmailContainer'
        db.create_table('tradeschool_branchemailcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentConfirmation'])),
            ('student_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentReminder'])),
            ('student_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentFeedback'])),
            ('teacher_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherConfirmation'])),
            ('teacher_class_approval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherClassApproval'])),
            ('teacher_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherReminder'])),
            ('teacher_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherFeedback'])),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(related_name='emails', unique=True, to=orm['tradeschool.Branch'])),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(related_name='emails', unique=True, to=orm['sites.Site'])),
        ))
        db.send_create_signal('tradeschool', ['BranchEmailContainer'])

        # Adding model 'Branch'
        db.create_table('tradeschool_branch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=120)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
        ))
        db.send_create_signal('tradeschool', ['Branch'])

        # Adding model 'Venue'
        db.create_table('tradeschool_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('venue_type', self.gf('django.db.models.fields.SmallIntegerField')(default=0, max_length=1)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.SmallIntegerField')(default=20, max_length=4)),
            ('resources', self.gf('django.db.models.fields.TextField')(default='Chairs, Tables', null=True)),
            ('color', self.gf('django.db.models.fields.CharField')(default='#491b0d', max_length=7)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default='2', to=orm['sites.Site'])),
        ))
        db.send_create_signal('tradeschool', ['Venue'])

        # Adding model 'Person'
        db.create_table('tradeschool_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('hashcode', self.gf('django.db.models.fields.CharField')(default='473f5c406a4d11e291c314109fdfc929', unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=120)),
        ))
        db.send_create_signal('tradeschool', ['Person'])

        # Adding M2M table for field site on 'Person'
        db.create_table('tradeschool_person_site', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['tradeschool.person'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('tradeschool_person_site', ['person_id', 'site_id'])

        # Adding model 'Course'
        db.create_table('tradeschool_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses_taught', to=orm['tradeschool.Person'])),
            ('category', self.gf('django.db.models.fields.SmallIntegerField')(default=2, max_length=1)),
            ('max_students', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=120, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tradeschool', ['Course'])

        # Adding M2M table for field site on 'Course'
        db.create_table('tradeschool_course_site', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['tradeschool.course'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('tradeschool_course_site', ['course_id', 'site_id'])

        # Adding model 'Time'
        db.create_table('tradeschool_time', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default='2', to=orm['sites.Site'])),
        ))
        db.send_create_signal('tradeschool', ['Time'])

        # Adding model 'TimeRange'
        db.create_table('tradeschool_timerange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2008, 1, 31, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2008, 1, 31, 0, 0))),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default='2', to=orm['sites.Site'])),
        ))
        db.send_create_signal('tradeschool', ['TimeRange'])

        # Adding model 'ScheduleEmailContainer'
        db.create_table('tradeschool_scheduleemailcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentConfirmation'])),
            ('student_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentReminder'])),
            ('student_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.StudentFeedback'])),
            ('teacher_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherConfirmation'])),
            ('teacher_class_approval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherClassApproval'])),
            ('teacher_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherReminder'])),
            ('teacher_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.TeacherFeedback'])),
            ('schedule', self.gf('django.db.models.fields.related.OneToOneField')(related_name='emails', unique=True, to=orm['tradeschool.Schedule'])),
        ))
        db.send_create_signal('tradeschool', ['ScheduleEmailContainer'])

        # Adding model 'Schedule'
        db.create_table('tradeschool_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Course'])),
            ('course_status', self.gf('django.db.models.fields.SmallIntegerField')(default=0, max_length=1)),
            ('hashcode', self.gf('django.db.models.fields.CharField')(default='4740ebd16a4d11e29db914109fdfc929', unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=120, unique=True, null=True)),
        ))
        db.send_create_signal('tradeschool', ['Schedule'])

        # Adding model 'BarterItem'
        db.create_table('tradeschool_barteritem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('requested', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Schedule'], null=True)),
        ))
        db.send_create_signal('tradeschool', ['BarterItem'])

        # Adding model 'Registration'
        db.create_table('tradeschool_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Schedule'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registrations', to=orm['tradeschool.Person'])),
            ('registration_status', self.gf('django.db.models.fields.CharField')(default='registered', max_length=20)),
        ))
        db.send_create_signal('tradeschool', ['Registration'])

        # Adding model 'RegisteredItem'
        db.create_table('tradeschool_registereditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Registration'])),
            ('barter_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.BarterItem'])),
            ('registered', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
        ))
        db.send_create_signal('tradeschool', ['RegisteredItem'])

        # Adding model 'Feedback'
        db.create_table('tradeschool_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Schedule'])),
            ('feedback_type', self.gf('django.db.models.fields.CharField')(default='student', max_length=20)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tradeschool', ['Feedback'])

        # Adding model 'Photo'
        db.create_table('tradeschool_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default='2', to=orm['sites.Site'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(default=[], to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal('tradeschool', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'StudentConfirmation'
        db.delete_table('tradeschool_studentconfirmation')

        # Deleting model 'StudentReminder'
        db.delete_table('tradeschool_studentreminder')

        # Deleting model 'StudentFeedback'
        db.delete_table('tradeschool_studentfeedback')

        # Deleting model 'TeacherConfirmation'
        db.delete_table('tradeschool_teacherconfirmation')

        # Deleting model 'TeacherClassApproval'
        db.delete_table('tradeschool_teacherclassapproval')

        # Deleting model 'TeacherReminder'
        db.delete_table('tradeschool_teacherreminder')

        # Deleting model 'TeacherFeedback'
        db.delete_table('tradeschool_teacherfeedback')

        # Deleting model 'DefaultEmailContainer'
        db.delete_table('tradeschool_defaultemailcontainer')

        # Deleting model 'BranchEmailContainer'
        db.delete_table('tradeschool_branchemailcontainer')

        # Deleting model 'Branch'
        db.delete_table('tradeschool_branch')

        # Deleting model 'Venue'
        db.delete_table('tradeschool_venue')

        # Deleting model 'Person'
        db.delete_table('tradeschool_person')

        # Removing M2M table for field site on 'Person'
        db.delete_table('tradeschool_person_site')

        # Deleting model 'Course'
        db.delete_table('tradeschool_course')

        # Removing M2M table for field site on 'Course'
        db.delete_table('tradeschool_course_site')

        # Deleting model 'Time'
        db.delete_table('tradeschool_time')

        # Deleting model 'TimeRange'
        db.delete_table('tradeschool_timerange')

        # Deleting model 'ScheduleEmailContainer'
        db.delete_table('tradeschool_scheduleemailcontainer')

        # Deleting model 'Schedule'
        db.delete_table('tradeschool_schedule')

        # Deleting model 'BarterItem'
        db.delete_table('tradeschool_barteritem')

        # Deleting model 'Registration'
        db.delete_table('tradeschool_registration')

        # Deleting model 'RegisteredItem'
        db.delete_table('tradeschool_registereditem')

        # Deleting model 'Feedback'
        db.delete_table('tradeschool_feedback')

        # Deleting model 'Photo'
        db.delete_table('tradeschool_photo')


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tradeschool.barteritem': {
            'Meta': {'object_name': 'BarterItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'requested': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Schedule']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.branch': {
            'Meta': {'ordering': "['title']", 'object_name': 'Branch'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.branchemailcontainer': {
            'Meta': {'object_name': 'BranchEmailContainer'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'emails'", 'unique': 'True', 'to': "orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'emails'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'student_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentConfirmation']"}),
            'student_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentFeedback']"}),
            'student_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentReminder']"}),
            'teacher_class_approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherClassApproval']"}),
            'teacher_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherConfirmation']"}),
            'teacher_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherFeedback']"}),
            'teacher_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherReminder']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.SmallIntegerField', [], {'default': '2', 'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'default': "'2'", 'to': "orm['sites.Site']", 'null': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'null': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_taught'", 'to': "orm['tradeschool.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.defaultemailcontainer': {
            'Meta': {'object_name': 'DefaultEmailContainer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'student_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentConfirmation']"}),
            'student_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentFeedback']"}),
            'student_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentReminder']"}),
            'teacher_class_approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherClassApproval']"}),
            'teacher_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherConfirmation']"}),
            'teacher_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherFeedback']"}),
            'teacher_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherReminder']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'default': "'student'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Schedule']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'473f5c406a4d11e291c314109fdfc929'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'default': "'2'", 'to': "orm['sites.Site']", 'null': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'tradeschool.photo': {
            'Meta': {'ordering': "['position']", 'object_name': 'Photo'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'default': '[]', 'to': "orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': "'2'", 'to': "orm['sites.Site']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.registereditem': {
            'Meta': {'object_name': 'RegisteredItem'},
            'barter_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.BarterItem']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'registered': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Registration']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.registration': {
            'Meta': {'object_name': 'Registration'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tradeschool.BarterItem']", 'through': "orm['tradeschool.RegisteredItem']", 'symmetrical': 'False'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '20'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Schedule']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': "orm['tradeschool.Person']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.schedule': {
            'Meta': {'ordering': "['course_status', 'start_time', '-venue']", 'object_name': 'Schedule'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Course']"}),
            'course_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'4740ebd16a4d11e29db914109fdfc929'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'unique': 'True', 'null': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tradeschool.Person']", 'through': "orm['tradeschool.Registration']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Venue']", 'null': 'True', 'blank': 'True'})
        },
        'tradeschool.scheduleemailcontainer': {
            'Meta': {'object_name': 'ScheduleEmailContainer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'schedule': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'emails'", 'unique': 'True', 'to': "orm['tradeschool.Schedule']"}),
            'student_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentConfirmation']"}),
            'student_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentFeedback']"}),
            'student_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.StudentReminder']"}),
            'teacher_class_approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherClassApproval']"}),
            'teacher_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherConfirmation']"}),
            'teacher_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherFeedback']"}),
            'teacher_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.TeacherReminder']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.studentconfirmation': {
            'Meta': {'object_name': 'StudentConfirmation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.studentfeedback': {
            'Meta': {'object_name': 'StudentFeedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.studentreminder': {
            'Meta': {'object_name': 'StudentReminder'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.teacherclassapproval': {
            'Meta': {'object_name': 'TeacherClassApproval'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.teacherconfirmation': {
            'Meta': {'object_name': 'TeacherConfirmation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.teacherfeedback': {
            'Meta': {'object_name': 'TeacherFeedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.teacherreminder': {
            'Meta': {'object_name': 'TeacherReminder'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.time': {
            'Meta': {'object_name': 'Time'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': "'2'", 'to': "orm['sites.Site']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.timerange': {
            'Meta': {'object_name': 'TimeRange'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2008, 1, 31, 0, 0)'}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': "'2'", 'to': "orm['sites.Site']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2008, 1, 31, 0, 0)'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tradeschool.venue': {
            'Meta': {'object_name': 'Venue'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {'default': '20', 'max_length': '4'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#d8713d'", 'max_length': '7'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'default': "'Chairs, Tables'", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': "'2'", 'to': "orm['sites.Site']"}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venue_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '1'})
        }
    }

    complete_apps = ['tradeschool']