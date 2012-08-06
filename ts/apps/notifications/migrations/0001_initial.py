# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseNotification'
        db.create_table('notifications_coursenotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1, max_length=1)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_type', self.gf('django.db.models.fields.SmallIntegerField')(max_length=1)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Course'])),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('email_status', self.gf('django.db.models.fields.SmallIntegerField')(max_length=1)),
        ))
        db.send_create_signal('notifications', ['CourseNotification'])

        # Adding model 'BranchNotificationTemplate'
        db.create_table('notifications_branchnotificationtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1, max_length=1)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_type', self.gf('django.db.models.fields.SmallIntegerField')(max_length=1)),
            ('cron', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('notifications', ['BranchNotificationTemplate'])

        # Adding model 'BranchNotification'
        db.create_table('notifications_branchnotification', (
            ('branchnotificationtemplate_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.BranchNotificationTemplate'], unique=True, primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.Branch'])),
        ))
        db.send_create_signal('notifications', ['BranchNotification'])

    def backwards(self, orm):
        # Deleting model 'CourseNotification'
        db.delete_table('notifications_coursenotification')

        # Deleting model 'BranchNotificationTemplate'
        db.delete_table('notifications_branchnotificationtemplate')

        # Deleting model 'BranchNotification'
        db.delete_table('notifications_branchnotification')

    models = {
        'branches.branch': {
            'Meta': {'object_name': 'Branch'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.branchnotification': {
            'Meta': {'object_name': 'BranchNotification', '_ormbases': ['notifications.BranchNotificationTemplate']},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['branches.Branch']"}),
            'branchnotificationtemplate_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['notifications.BranchNotificationTemplate']", 'unique': 'True', 'primary_key': 'True'})
        },
        'notifications.branchnotificationtemplate': {
            'Meta': {'object_name': 'BranchNotificationTemplate'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cron': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_type': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'max_length': '1'}),
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
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.SmallIntegerField', [], {'default': '6', 'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'null': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'max_length': '1'}),
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
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'09537bc79a4111e188df001cb3bb4ebc'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['notifications']