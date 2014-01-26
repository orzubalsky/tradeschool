# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StudentConfirmation'
        db.create_table(u'tradeschool_studentconfirmation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'tradeschool', ['StudentConfirmation'])

        # Adding model 'StudentReminder'
        db.create_table(u'tradeschool_studentreminder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal(u'tradeschool', ['StudentReminder'])

        # Adding model 'StudentFeedback'
        db.create_table(u'tradeschool_studentfeedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal(u'tradeschool', ['StudentFeedback'])

        # Adding model 'TeacherConfirmation'
        db.create_table(u'tradeschool_teacherconfirmation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'tradeschool', ['TeacherConfirmation'])

        # Adding model 'TeacherClassApproval'
        db.create_table(u'tradeschool_teacherclassapproval', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'tradeschool', ['TeacherClassApproval'])

        # Adding model 'TeacherReminder'
        db.create_table(u'tradeschool_teacherreminder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal(u'tradeschool', ['TeacherReminder'])

        # Adding model 'TeacherFeedback'
        db.create_table(u'tradeschool_teacherfeedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Branch'], unique=True, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.Course'], unique=True, null=True, blank=True)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('days_delta', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('send_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 0))),
        ))
        db.send_create_signal(u'tradeschool', ['TeacherFeedback'])

        # Adding model 'DefaultEmailContainer'
        db.create_table(u'tradeschool_defaultemailcontainer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('studentconfirmation', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.StudentConfirmation'], unique=True)),
            ('studentreminder', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.StudentReminder'], unique=True)),
            ('studentfeedback', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.StudentFeedback'], unique=True)),
            ('teacherconfirmation', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.TeacherConfirmation'], unique=True)),
            ('teacherclassapproval', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.TeacherClassApproval'], unique=True)),
            ('teacherreminder', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.TeacherReminder'], unique=True)),
            ('teacherfeedback', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tradeschool.TeacherFeedback'], unique=True)),
        ))
        db.send_create_signal(u'tradeschool', ['DefaultEmailContainer'])

        # Adding model 'Cluster'
        db.create_table(u'tradeschool_cluster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=120)),
        ))
        db.send_create_signal(u'tradeschool', ['Cluster'])

        # Adding model 'Language'
        db.create_table(u'tradeschool_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6, db_index=True)),
        ))
        db.send_create_signal(u'tradeschool', ['Language'])

        # Adding model 'Branch'
        db.create_table(u'tradeschool_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=120)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('branch_status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=50)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('header_copy', self.gf('tinymce.models.HTMLField')(default='Barter for knowledge', null=True, blank=True)),
            ('intro_copy', self.gf('tinymce.models.HTMLField')(default='Information for the header of the page', null=True, blank=True)),
            ('footer_copy', self.gf('tinymce.models.HTMLField')(default='Information for the footer of the page', null=True, blank=True)),
        ))
        db.send_create_signal(u'tradeschool', ['Branch'])

        # Adding M2M table for field languages on 'Branch'
        m2m_table_name = db.shorten_name(u'tradeschool_branch_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('branch', models.ForeignKey(orm[u'tradeschool.branch'], null=False)),
            ('language', models.ForeignKey(orm[u'tradeschool.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['branch_id', 'language_id'])

        # Adding M2M table for field organizers on 'Branch'
        m2m_table_name = db.shorten_name(u'tradeschool_branch_organizers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('branch', models.ForeignKey(orm[u'tradeschool.branch'], null=False)),
            ('person', models.ForeignKey(orm[u'tradeschool.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['branch_id', 'person_id'])

        # Adding M2M table for field clusters on 'Branch'
        m2m_table_name = db.shorten_name(u'tradeschool_branch_clusters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('branch', models.ForeignKey(orm[u'tradeschool.branch'], null=False)),
            ('cluster', models.ForeignKey(orm[u'tradeschool.cluster'], null=False))
        ))
        db.create_unique(m2m_table_name, ['branch_id', 'cluster_id'])

        # Adding model 'Venue'
        db.create_table(u'tradeschool_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'])),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('capacity', self.gf('django.db.models.fields.SmallIntegerField')(default=20, max_length=4)),
            ('resources', self.gf('django.db.models.fields.TextField')(default='For Example: Chairs, Tables', null=True)),
            ('color', self.gf('django.db.models.fields.CharField')(default='#471ee0', max_length=7)),
        ))
        db.send_create_signal(u'tradeschool', ['Venue'])

        # Adding model 'Person'
        db.create_table(u'tradeschool_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=220)),
            ('default_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='default_branch', null=True, to=orm['tradeschool.Branch'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=50, null=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('courses_taught_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=7)),
            ('courses_taken_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=7)),
            ('names_of_co_organizers', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'tradeschool', ['Person'])

        # Adding M2M table for field groups on 'Person'
        m2m_table_name = db.shorten_name(u'tradeschool_person_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'tradeschool.person'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Person'
        m2m_table_name = db.shorten_name(u'tradeschool_person_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'tradeschool.person'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'permission_id'])

        # Adding M2M table for field branches on 'Person'
        m2m_table_name = db.shorten_name(u'tradeschool_person_branches')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'tradeschool.person'], null=False)),
            ('branch', models.ForeignKey(orm[u'tradeschool.branch'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'branch_id'])

        # Adding model 'Time'
        db.create_table(u'tradeschool_time', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 25, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 25, 0, 0))),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True, blank=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal(u'tradeschool', ['Time'])

        # Adding model 'TimeRange'
        db.create_table(u'tradeschool_timerange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 1, 25, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 1, 25, 0, 0))),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2008, 1, 31, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2008, 1, 31, 0, 0))),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True, blank=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal(u'tradeschool', ['TimeRange'])

        # Adding model 'BarterItem'
        db.create_table(u'tradeschool_barteritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Course'])),
        ))
        db.send_create_signal(u'tradeschool', ['BarterItem'])

        # Adding model 'Course'
        db.create_table(u'tradeschool_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 25, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 25, 0, 0))),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'])),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('max_students', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=20)),
            ('color', self.gf('django.db.models.fields.CharField')(default=5, max_length=7)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses_taught', to=orm['tradeschool.Person'])),
        ))
        db.send_create_signal(u'tradeschool', ['Course'])

        # Adding model 'Registration'
        db.create_table(u'tradeschool_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Course'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registrations', to=orm['tradeschool.Person'])),
            ('registration_status', self.gf('django.db.models.fields.CharField')(default='registered', max_length=20)),
        ))
        db.send_create_signal(u'tradeschool', ['Registration'])

        # Adding unique constraint on 'Registration', fields ['course', 'student']
        db.create_unique(u'tradeschool_registration', ['course_id', 'student_id'])

        # Adding M2M table for field items on 'Registration'
        m2m_table_name = db.shorten_name(u'tradeschool_registration_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registration', models.ForeignKey(orm[u'tradeschool.registration'], null=False)),
            ('barteritem', models.ForeignKey(orm[u'tradeschool.barteritem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registration_id', 'barteritem_id'])

        # Adding model 'Feedback'
        db.create_table(u'tradeschool_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Course'])),
            ('feedback_type', self.gf('django.db.models.fields.CharField')(default='student', max_length=20)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'tradeschool', ['Feedback'])

        # Adding model 'Photo'
        db.create_table(u'tradeschool_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal(u'tradeschool', ['Photo'])

        # Adding model 'Page'
        db.create_table(u'tradeschool_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'], null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tradeschool', ['Page'])

        # Adding unique constraint on 'Page', fields ['branch', 'url']
        db.create_unique(u'tradeschool_page', ['branch_id', 'url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['branch', 'url']
        db.delete_unique(u'tradeschool_page', ['branch_id', 'url'])

        # Removing unique constraint on 'Registration', fields ['course', 'student']
        db.delete_unique(u'tradeschool_registration', ['course_id', 'student_id'])

        # Deleting model 'StudentConfirmation'
        db.delete_table(u'tradeschool_studentconfirmation')

        # Deleting model 'StudentReminder'
        db.delete_table(u'tradeschool_studentreminder')

        # Deleting model 'StudentFeedback'
        db.delete_table(u'tradeschool_studentfeedback')

        # Deleting model 'TeacherConfirmation'
        db.delete_table(u'tradeschool_teacherconfirmation')

        # Deleting model 'TeacherClassApproval'
        db.delete_table(u'tradeschool_teacherclassapproval')

        # Deleting model 'TeacherReminder'
        db.delete_table(u'tradeschool_teacherreminder')

        # Deleting model 'TeacherFeedback'
        db.delete_table(u'tradeschool_teacherfeedback')

        # Deleting model 'DefaultEmailContainer'
        db.delete_table(u'tradeschool_defaultemailcontainer')

        # Deleting model 'Cluster'
        db.delete_table(u'tradeschool_cluster')

        # Deleting model 'Language'
        db.delete_table(u'tradeschool_language')

        # Deleting model 'Branch'
        db.delete_table(u'tradeschool_branch')

        # Removing M2M table for field languages on 'Branch'
        db.delete_table(db.shorten_name(u'tradeschool_branch_languages'))

        # Removing M2M table for field organizers on 'Branch'
        db.delete_table(db.shorten_name(u'tradeschool_branch_organizers'))

        # Removing M2M table for field clusters on 'Branch'
        db.delete_table(db.shorten_name(u'tradeschool_branch_clusters'))

        # Deleting model 'Venue'
        db.delete_table(u'tradeschool_venue')

        # Deleting model 'Person'
        db.delete_table(u'tradeschool_person')

        # Removing M2M table for field groups on 'Person'
        db.delete_table(db.shorten_name(u'tradeschool_person_groups'))

        # Removing M2M table for field user_permissions on 'Person'
        db.delete_table(db.shorten_name(u'tradeschool_person_user_permissions'))

        # Removing M2M table for field branches on 'Person'
        db.delete_table(db.shorten_name(u'tradeschool_person_branches'))

        # Deleting model 'Time'
        db.delete_table(u'tradeschool_time')

        # Deleting model 'TimeRange'
        db.delete_table(u'tradeschool_timerange')

        # Deleting model 'BarterItem'
        db.delete_table(u'tradeschool_barteritem')

        # Deleting model 'Course'
        db.delete_table(u'tradeschool_course')

        # Deleting model 'Registration'
        db.delete_table(u'tradeschool_registration')

        # Removing M2M table for field items on 'Registration'
        db.delete_table(db.shorten_name(u'tradeschool_registration_items'))

        # Deleting model 'Feedback'
        db.delete_table(u'tradeschool_feedback')

        # Deleting model 'Photo'
        db.delete_table(u'tradeschool_photo')

        # Deleting model 'Page'
        db.delete_table(u'tradeschool_page')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tradeschool.barteritem': {
            'Meta': {'ordering': "['title']", 'object_name': 'BarterItem'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Course']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.branch': {
            'Meta': {'ordering': "['title']", 'object_name': 'Branch'},
            'branch_status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'clusters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tradeschool.Cluster']", 'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'footer_copy': ('tinymce.models.HTMLField', [], {'default': "'Information for the footer of the page'", 'null': 'True', 'blank': 'True'}),
            'header_copy': ('tinymce.models.HTMLField', [], {'default': "'Barter for knowledge'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_copy': ('tinymce.models.HTMLField', [], {'default': "'Information for the header of the page'", 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tradeschool.Language']", 'symmetrical': 'False'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'branches_organized'", 'symmetrical': 'False', 'db_column': "'person_id'", 'to': u"orm['tradeschool.Person']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.cluster': {
            'Meta': {'ordering': "['name']", 'object_name': 'Cluster'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '120'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.course': {
            'Meta': {'ordering': "['status', 'start_time', '-venue', 'title']", 'object_name': 'Course'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'color': ('django.db.models.fields.CharField', [], {'default': '5', 'max_length': '7'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tradeschool.Person']", 'through': u"orm['tradeschool.Registration']", 'symmetrical': 'False'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_taught'", 'to': u"orm['tradeschool.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Venue']", 'null': 'True', 'blank': 'True'})
        },
        u'tradeschool.defaultemailcontainer': {
            'Meta': {'object_name': 'DefaultEmailContainer'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'studentconfirmation': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.StudentConfirmation']", 'unique': 'True'}),
            'studentfeedback': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.StudentFeedback']", 'unique': 'True'}),
            'studentreminder': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.StudentReminder']", 'unique': 'True'}),
            'teacherclassapproval': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.TeacherClassApproval']", 'unique': 'True'}),
            'teacherconfirmation': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.TeacherConfirmation']", 'unique': 'True'}),
            'teacherfeedback': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.TeacherFeedback']", 'unique': 'True'}),
            'teacherreminder': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.TeacherReminder']", 'unique': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Course']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'default': "'student'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.page': {
            'Meta': {'ordering': "['branch', 'title']", 'unique_together': "(('branch', 'url'),)", 'object_name': 'Page'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']", 'null': 'True', 'blank': 'True'}),
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'tradeschool.person': {
            'Meta': {'ordering': "['fullname']", 'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'branches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tradeschool.Branch']", 'symmetrical': 'False'}),
            'courses_taken_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '7'}),
            'courses_taught_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '7'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'default_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_branch'", 'null': 'True', 'to': u"orm['tradeschool.Branch']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '50', 'null': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'names_of_co_organizers': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '220'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'tradeschool.photo': {
            'Meta': {'ordering': "['position']", 'object_name': 'Photo'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.registration': {
            'Meta': {'ordering': "['-course__start_time', 'course', 'registration_status', 'student']", 'unique_together': "(('course', 'student'),)", 'object_name': 'Registration'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Course']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tradeschool.BarterItem']", 'symmetrical': 'False'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '20'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': u"orm['tradeschool.Person']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tradeschool.studentconfirmation': {
            'Meta': {'object_name': 'StudentConfirmation'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.studentfeedback': {
            'Meta': {'object_name': 'StudentFeedback'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.studentreminder': {
            'Meta': {'object_name': 'StudentReminder'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.teacherclassapproval': {
            'Meta': {'object_name': 'TeacherClassApproval'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.teacherconfirmation': {
            'Meta': {'object_name': 'TeacherConfirmation'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.teacherfeedback': {
            'Meta': {'object_name': 'TeacherFeedback'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.teacherreminder': {
            'Meta': {'object_name': 'TeacherReminder'},
            'branch': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Branch']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tradeschool.Course']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'days_delta': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'tradeschool.time': {
            'Meta': {'object_name': 'Time'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Venue']", 'null': 'True', 'blank': 'True'})
        },
        u'tradeschool.timerange': {
            'Meta': {'object_name': 'TimeRange'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2008, 1, 31, 0, 0)'}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2008, 1, 31, 0, 0)'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Venue']", 'null': 'True', 'blank': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'tradeschool.venue': {
            'Meta': {'ordering': "['branch', 'is_active', 'title']", 'object_name': 'Venue'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {'default': '20', 'max_length': '4'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#5e2692'", 'max_length': '7'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'default': "'For Example: Chairs, Tables'", 'null': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['tradeschool']