# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Time.venue'
        db.alter_column(u'tradeschool_time', 'venue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True, on_delete=models.SET_NULL))

        # Changing field 'TimeRange.venue'
        db.alter_column(u'tradeschool_timerange', 'venue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):

        # Changing field 'Time.venue'
        db.alter_column(u'tradeschool_time', 'venue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True))

        # Changing field 'TimeRange.venue'
        db.alter_column(u'tradeschool_timerange', 'venue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Venue'], null=True))

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
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '50', 'null': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tradeschool.Language']", 'null': 'True', 'blank': 'True'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'branches_organized'", 'symmetrical': 'False', 'db_column': "'person_id'", 'to': u"orm['tradeschool.Person']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'Etc/GMT+0'", 'max_length': '100'}),
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
            'color': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '7'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 1, 0, 0)'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tradeschool.Person']", 'through': u"orm['tradeschool.Registration']", 'symmetrical': 'False'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_taught'", 'to': u"orm['tradeschool.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_registered_students': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Venue']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
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
            'is_student': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_teacher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 1, 0, 0)'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Venue']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'tradeschool.timerange': {
            'Meta': {'object_name': 'TimeRange'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 1, 0, 0)'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2008, 1, 31, 0, 0)'}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 1, 0, 0)'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2008, 1, 31, 0, 0)'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Venue']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'tradeschool.venue': {
            'Meta': {'ordering': "['branch', 'is_active', 'title']", 'object_name': 'Venue'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tradeschool.Branch']"}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {'default': '20', 'max_length': '4'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#d0cb90'", 'max_length': '7'}),
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