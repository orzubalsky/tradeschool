# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BranchNotificationTemplate.status'
        db.delete_column('notifications_branchnotificationtemplate', 'status')

        # Adding field 'BranchNotificationTemplate.is_active'
        db.add_column('notifications_branchnotificationtemplate', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'CourseNotification.status'
        db.delete_column('notifications_coursenotification', 'status')

        # Adding field 'CourseNotification.is_active'
        db.add_column('notifications_coursenotification', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # Changing field 'BranchNotification.branch'
        db.alter_column('notifications_branchnotification', 'branch_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch']))
    def backwards(self, orm):
        # Adding field 'BranchNotificationTemplate.status'
        db.add_column('notifications_branchnotificationtemplate', 'status',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1, max_length=1),
                      keep_default=False)

        # Deleting field 'BranchNotificationTemplate.is_active'
        db.delete_column('notifications_branchnotificationtemplate', 'is_active')

        # Adding field 'CourseNotification.status'
        db.add_column('notifications_coursenotification', 'status',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1, max_length=1),
                      keep_default=False)

        # Deleting field 'CourseNotification.is_active'
        db.delete_column('notifications_coursenotification', 'is_active')


        # Changing field 'BranchNotification.branch'
        db.alter_column('notifications_branchnotification', 'branch_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.Branch']))
    models = {
        'notifications.branchnotification': {
            'Meta': {'object_name': 'BranchNotification', '_ormbases': ['notifications.BranchNotificationTemplate']},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Branch']"}),
            'branchnotificationtemplate_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.BranchNotificationTemplate']", 'unique': 'True', 'primary_key': 'True'})
        },
        'notifications.branchnotificationtemplate': {
            'Meta': {'object_name': 'BranchNotificationTemplate'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cron': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_type': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.coursenotification': {
            'Meta': {'object_name': 'CourseNotification'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Course']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '1'}),
            'email_type': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.branch': {
            'Meta': {'object_name': 'Branch'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.SmallIntegerField', [], {'default': '6', 'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'null': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'5c888ea6b58e11e1b4380019e346b4fc'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['notifications']