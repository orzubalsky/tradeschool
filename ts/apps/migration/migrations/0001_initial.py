# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BranchPages'
        db.create_table(u'branch_pages', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['BranchPages'])

        # Adding model 'BranchPhotos'
        db.create_table(u'branch_photos', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')()),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('filename_original', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['BranchPhotos'])

        # Adding model 'BranchSeasons'
        db.create_table(u'branch_seasons', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('unix_start_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('unix_end_time', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'migration', ['BranchSeasons'])

        # Adding model 'Branches'
        db.create_table(u'branches', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('header', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('footer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'migration', ['Branches'])

        # Adding model 'ClassCategories'
        db.create_table(u'class_categories', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=21)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['ClassCategories'])

        # Adding model 'ClassNotifications'
        db.create_table(u'class_notifications', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('class_id', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('send_on', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'migration', ['ClassNotifications'])

        # Adding model 'Classes'
        db.create_table(u'classes', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('venue_id', self.gf('django.db.models.fields.IntegerField')()),
            ('category_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('max_students', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('unix_start_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('unix_end_time', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'migration', ['Classes'])

        # Adding model 'ClassesXItems'
        db.create_table(u'classes_x_items', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('class_id', self.gf('django.db.models.fields.IntegerField')()),
            ('item_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['ClassesXItems'])

        # Adding model 'Feedbacks'
        db.create_table(u'feedbacks', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('class_id', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('author_id', self.gf('django.db.models.fields.IntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['Feedbacks'])

        # Adding model 'Items'
        db.create_table(u'items', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('requested', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['Items'])

        # Adding model 'Mailinglist'
        db.create_table(u'mailinglist', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['Mailinglist'])

        # Adding model 'Notifications'
        db.create_table(u'notifications', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('cron', self.gf('django.db.models.fields.IntegerField')()),
            ('hour_interval', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('day_interval', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'migration', ['Notifications'])

        # Adding model 'NotificationsDefaults'
        db.create_table(u'notifications_defaults', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('cron', self.gf('django.db.models.fields.IntegerField')()),
            ('hour_interval_default', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('day_interval_default', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'migration', ['NotificationsDefaults'])

        # Adding model 'Students'
        db.create_table(u'students', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['Students'])

        # Adding model 'StudentsXClasses'
        db.create_table(u'students_x_classes', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.IntegerField')()),
            ('class_id', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['StudentsXClasses'])

        # Adding model 'StudentsXItems'
        db.create_table(u'students_x_items', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.IntegerField')()),
            ('item_id', self.gf('django.db.models.fields.IntegerField')()),
            ('class_id', self.gf('django.db.models.fields.IntegerField')()),
            ('registered', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['StudentsXItems'])

        # Adding model 'Teachers'
        db.create_table(u'teachers', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['Teachers'])

        # Adding model 'TeachersXClasses'
        db.create_table(u'teachers_x_classes', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('teacher_id', self.gf('django.db.models.fields.IntegerField')()),
            ('class_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['TeachersXClasses'])

        # Adding model 'Users'
        db.create_table(u'users', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['Users'])

        # Adding model 'VenueRules'
        db.create_table(u'venue_rules', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('venue_id', self.gf('django.db.models.fields.IntegerField')()),
            ('season_id', self.gf('django.db.models.fields.IntegerField')()),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('start_time', self.gf('django.db.models.fields.TextField')()),
            ('end_time', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['VenueRules'])

        # Adding model 'VenueRulesExceptions'
        db.create_table(u'venue_rules_exceptions', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('rule_id', self.gf('django.db.models.fields.IntegerField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'migration', ['VenueRulesExceptions'])

        # Adding model 'VenueTimes'
        db.create_table(u'venue_times', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('venue_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('unix_start_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('unix_end_time', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'migration', ['VenueTimes'])

        # Adding model 'Venues'
        db.create_table(u'venues', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('branch_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=765, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=765, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('resources', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=21, null=True, blank=True)),
        ))
        db.send_create_signal(u'migration', ['Venues'])


    def backwards(self, orm):
        # Deleting model 'BranchPages'
        db.delete_table(u'branch_pages')

        # Deleting model 'BranchPhotos'
        db.delete_table(u'branch_photos')

        # Deleting model 'BranchSeasons'
        db.delete_table(u'branch_seasons')

        # Deleting model 'Branches'
        db.delete_table(u'branches')

        # Deleting model 'ClassCategories'
        db.delete_table(u'class_categories')

        # Deleting model 'ClassNotifications'
        db.delete_table(u'class_notifications')

        # Deleting model 'Classes'
        db.delete_table(u'classes')

        # Deleting model 'ClassesXItems'
        db.delete_table(u'classes_x_items')

        # Deleting model 'Feedbacks'
        db.delete_table(u'feedbacks')

        # Deleting model 'Items'
        db.delete_table(u'items')

        # Deleting model 'Mailinglist'
        db.delete_table(u'mailinglist')

        # Deleting model 'Notifications'
        db.delete_table(u'notifications')

        # Deleting model 'NotificationsDefaults'
        db.delete_table(u'notifications_defaults')

        # Deleting model 'Students'
        db.delete_table(u'students')

        # Deleting model 'StudentsXClasses'
        db.delete_table(u'students_x_classes')

        # Deleting model 'StudentsXItems'
        db.delete_table(u'students_x_items')

        # Deleting model 'Teachers'
        db.delete_table(u'teachers')

        # Deleting model 'TeachersXClasses'
        db.delete_table(u'teachers_x_classes')

        # Deleting model 'Users'
        db.delete_table(u'users')

        # Deleting model 'VenueRules'
        db.delete_table(u'venue_rules')

        # Deleting model 'VenueRulesExceptions'
        db.delete_table(u'venue_rules_exceptions')

        # Deleting model 'VenueTimes'
        db.delete_table(u'venue_times')

        # Deleting model 'Venues'
        db.delete_table(u'venues')


    models = {
        u'migration.branches': {
            'Meta': {'object_name': 'Branches', 'db_table': "u'branches'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'footer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        u'migration.branchpages': {
            'Meta': {'object_name': 'BranchPages', 'db_table': "u'branch_pages'"},
            'branch_id': ('django.db.models.fields.IntegerField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        u'migration.branchphotos': {
            'Meta': {'object_name': 'BranchPhotos', 'db_table': "u'branch_photos'"},
            'branch_id': ('django.db.models.fields.IntegerField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'filename_original': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.branchseasons': {
            'Meta': {'object_name': 'BranchSeasons', 'db_table': "u'branch_seasons'"},
            'branch_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'unix_end_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'unix_start_time': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'migration.classcategories': {
            'Meta': {'object_name': 'ClassCategories', 'db_table': "u'class_categories'"},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '21'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        u'migration.classes': {
            'Meta': {'object_name': 'Classes', 'db_table': "u'classes'"},
            'category_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'unix_end_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'unix_start_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'venue_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.classesxitems': {
            'Meta': {'object_name': 'ClassesXItems', 'db_table': "u'classes_x_items'"},
            'class_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.classnotifications': {
            'Meta': {'object_name': 'ClassNotifications', 'db_table': "u'class_notifications'"},
            'class_id': ('django.db.models.fields.IntegerField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'send_on': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.feedbacks': {
            'Meta': {'object_name': 'Feedbacks', 'db_table': "u'feedbacks'"},
            'author_id': ('django.db.models.fields.IntegerField', [], {}),
            'class_id': ('django.db.models.fields.IntegerField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.items': {
            'Meta': {'object_name': 'Items', 'db_table': "u'items'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'requested': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        u'migration.mailinglist': {
            'Meta': {'object_name': 'Mailinglist', 'db_table': "u'mailinglist'"},
            'branch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.notifications': {
            'Meta': {'object_name': 'Notifications', 'db_table': "u'notifications'"},
            'branch_id': ('django.db.models.fields.IntegerField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'cron': ('django.db.models.fields.IntegerField', [], {}),
            'day_interval': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hour_interval': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.notificationsdefaults': {
            'Meta': {'object_name': 'NotificationsDefaults', 'db_table': "u'notifications_defaults'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            'cron': ('django.db.models.fields.IntegerField', [], {}),
            'day_interval_default': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hour_interval_default': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.students': {
            'Meta': {'object_name': 'Students', 'db_table': "u'students'"},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.studentsxclasses': {
            'Meta': {'object_name': 'StudentsXClasses', 'db_table': "u'students_x_classes'"},
            'class_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'student_id': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.studentsxitems': {
            'Meta': {'object_name': 'StudentsXItems', 'db_table': "u'students_x_items'"},
            'class_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.IntegerField', [], {}),
            'registered': ('django.db.models.fields.IntegerField', [], {}),
            'student_id': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.teachers': {
            'Meta': {'object_name': 'Teachers', 'db_table': "u'teachers'"},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'})
        },
        u'migration.teachersxclasses': {
            'Meta': {'object_name': 'TeachersXClasses', 'db_table': "u'teachers_x_classes'"},
            'class_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'teacher_id': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'migration.users': {
            'Meta': {'object_name': 'Users', 'db_table': "u'users'"},
            'branch_id': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        u'migration.venuerules': {
            'Meta': {'object_name': 'VenueRules', 'db_table': "u'venue_rules'"},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'end_time': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'season_id': ('django.db.models.fields.IntegerField', [], {}),
            'start_time': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'venue_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.venuerulesexceptions': {
            'Meta': {'object_name': 'VenueRulesExceptions', 'db_table': "u'venue_rules_exceptions'"},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'rule_id': ('django.db.models.fields.IntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'migration.venues': {
            'Meta': {'object_name': 'Venues', 'db_table': "u'venues'"},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'branch_id': ('django.db.models.fields.IntegerField', [], {}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '21', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'migration.venuetimes': {
            'Meta': {'object_name': 'VenueTimes', 'db_table': "u'venue_times'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'unix_end_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'unix_start_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'venue_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['migration']