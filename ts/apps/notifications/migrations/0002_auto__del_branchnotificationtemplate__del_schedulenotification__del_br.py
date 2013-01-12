# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BranchNotificationTemplate'
        db.delete_table('notifications_branchnotificationtemplate')

        # Deleting model 'ScheduleNotification'
        db.delete_table('notifications_schedulenotification')

        # Deleting model 'BranchNotification'
        db.delete_table('notifications_branchnotification')

        # Adding model 'ScheduleEmailContainer'
        db.create_table('notifications_scheduleemailcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails', to=orm['tradeschool.Schedule'])),
        ))
        db.send_create_signal('notifications', ['ScheduleEmailContainer'])

        # Adding model 'StudentFeedback'
        db.create_table('notifications_studentfeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['StudentFeedback'])

        # Adding model 'StudentReminder'
        db.create_table('notifications_studentreminder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['StudentReminder'])

        # Adding model 'TeacherClassApproval'
        db.create_table('notifications_teacherclassapproval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
        ))
        db.send_create_signal('notifications', ['TeacherClassApproval'])

        # Adding model 'ScheduleTemplate'
        db.create_table('notifications_scheduletemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.BranchTemplate'])),
        ))
        db.send_create_signal('notifications', ['ScheduleTemplate'])

        # Adding model 'TeacherConfirmation'
        db.create_table('notifications_teacherconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
        ))
        db.send_create_signal('notifications', ['TeacherConfirmation'])

        # Adding model 'TeacherReminder'
        db.create_table('notifications_teacherreminder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['TeacherReminder'])

        # Adding model 'TeacherFeedback'
        db.create_table('notifications_teacherfeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['TeacherFeedback'])

        # Adding model 'DefaultTemplate'
        db.create_table('notifications_defaulttemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notifications', ['DefaultTemplate'])

        # Adding model 'BranchTemplate'
        db.create_table('notifications_branchtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.DefaultTemplate'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal('notifications', ['BranchTemplate'])

        # Adding model 'StudentConfirmation'
        db.create_table('notifications_studentconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleEmailContainer'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.ScheduleTemplate'])),
        ))
        db.send_create_signal('notifications', ['StudentConfirmation'])


    def backwards(self, orm):
        # Adding model 'BranchNotificationTemplate'
        db.create_table('notifications_branchnotificationtemplate', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('cron', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('notifications', ['BranchNotificationTemplate'])

        # Adding model 'ScheduleNotification'
        db.create_table('notifications_schedulenotification', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Schedule'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('send_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('email_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email_status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=30)),
        ))
        db.send_create_signal('notifications', ['ScheduleNotification'])

        # Adding model 'BranchNotification'
        db.create_table('notifications_branchnotification', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('cron', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('email_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal('notifications', ['BranchNotification'])

        # Deleting model 'ScheduleEmailContainer'
        db.delete_table('notifications_scheduleemailcontainer')

        # Deleting model 'StudentFeedback'
        db.delete_table('notifications_studentfeedback')

        # Deleting model 'StudentReminder'
        db.delete_table('notifications_studentreminder')

        # Deleting model 'TeacherClassApproval'
        db.delete_table('notifications_teacherclassapproval')

        # Deleting model 'ScheduleTemplate'
        db.delete_table('notifications_scheduletemplate')

        # Deleting model 'TeacherConfirmation'
        db.delete_table('notifications_teacherconfirmation')

        # Deleting model 'TeacherReminder'
        db.delete_table('notifications_teacherreminder')

        # Deleting model 'TeacherFeedback'
        db.delete_table('notifications_teacherfeedback')

        # Deleting model 'DefaultTemplate'
        db.delete_table('notifications_defaulttemplate')

        # Deleting model 'BranchTemplate'
        db.delete_table('notifications_branchtemplate')

        # Deleting model 'StudentConfirmation'
        db.delete_table('notifications_studentconfirmation')


    models = {
        'notifications.branchtemplate': {
            'Meta': {'object_name': 'BranchTemplate'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['tradeschool.Branch']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.DefaultTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.defaulttemplate': {
            'Meta': {'object_name': 'DefaultTemplate'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.scheduleemailcontainer': {
            'Meta': {'object_name': 'ScheduleEmailContainer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['tradeschool.Schedule']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.scheduletemplate': {
            'Meta': {'object_name': 'ScheduleTemplate'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.BranchTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.studentconfirmation': {
            'Meta': {'object_name': 'StudentConfirmation'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.studentfeedback': {
            'Meta': {'object_name': 'StudentFeedback'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.studentreminder': {
            'Meta': {'object_name': 'StudentReminder'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherclassapproval': {
            'Meta': {'object_name': 'TeacherClassApproval'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherconfirmation': {
            'Meta': {'object_name': 'TeacherConfirmation'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherfeedback': {
            'Meta': {'object_name': 'TeacherFeedback'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherreminder': {
            'Meta': {'object_name': 'TeacherReminder'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleEmailContainer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.ScheduleTemplate']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
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
            'Meta': {'object_name': 'Branch'},
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
        'tradeschool.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.SmallIntegerField', [], {'default': '5', 'max_length': '1'}),
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
        'tradeschool.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'98fb1a915ce211e29a6d0023dffd8312'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'default': "'2'", 'to': "orm['sites.Site']", 'null': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 12, 0, 0)'}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'98fcc5665ce211e280dd0023dffd8312'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'unique': 'True', 'null': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 12, 0, 0)'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tradeschool.Person']", 'through': "orm['tradeschool.Registration']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Venue']", 'null': 'True', 'blank': 'True'})
        },
        'tradeschool.venue': {
            'Meta': {'object_name': 'Venue'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {'default': '20', 'max_length': '4'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#7ac36c'", 'max_length': '7'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'default': "'Chairs, Tables'", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venue_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '1'})
        }
    }

    complete_apps = ['notifications']