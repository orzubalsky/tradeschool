# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Day'
        db.delete_table('tradeschool_day')

        # Adding field 'TimeRange.sunday'
        db.add_column('tradeschool_timerange', 'sunday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TimeRange.monday'
        db.add_column('tradeschool_timerange', 'monday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TimeRange.tueday'
        db.add_column('tradeschool_timerange', 'tueday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TimeRange.wednesday'
        db.add_column('tradeschool_timerange', 'wednesday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TimeRange.thursday'
        db.add_column('tradeschool_timerange', 'thursday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TimeRange.friday'
        db.add_column('tradeschool_timerange', 'friday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TimeRange.saturday'
        db.add_column('tradeschool_timerange', 'saturday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Removing M2M table for field days on 'TimeRange'
        db.delete_table('tradeschool_timerange_days')


    def backwards(self, orm):
        # Adding model 'Day'
        db.create_table('tradeschool_day', (
            ('day', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('tradeschool', ['Day'])

        # Deleting field 'TimeRange.sunday'
        db.delete_column('tradeschool_timerange', 'sunday')

        # Deleting field 'TimeRange.monday'
        db.delete_column('tradeschool_timerange', 'monday')

        # Deleting field 'TimeRange.tueday'
        db.delete_column('tradeschool_timerange', 'tueday')

        # Deleting field 'TimeRange.wednesday'
        db.delete_column('tradeschool_timerange', 'wednesday')

        # Deleting field 'TimeRange.thursday'
        db.delete_column('tradeschool_timerange', 'thursday')

        # Deleting field 'TimeRange.friday'
        db.delete_column('tradeschool_timerange', 'friday')

        # Deleting field 'TimeRange.saturday'
        db.delete_column('tradeschool_timerange', 'saturday')

        # Adding M2M table for field days on 'TimeRange'
        db.create_table('tradeschool_timerange_days', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('timerange', models.ForeignKey(orm['tradeschool.timerange'], null=False)),
            ('day', models.ForeignKey(orm['tradeschool.day'], null=False))
        ))
        db.create_unique('tradeschool_timerange_days', ['timerange_id', 'day_id'])


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
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'default': "'4'", 'to': "orm['sites.Site']", 'null': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'null': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_taught'", 'to': "orm['tradeschool.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'author': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tradeschool.Person']", 'unique': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Schedule']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'1267e1854ef011e2872814109fdfc929'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'default': "'4'", 'to': "orm['sites.Site']", 'null': 'True', 'symmetrical': 'False'}),
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
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'1269ad544ef011e28bf914109fdfc929'", 'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tradeschool.Person']", 'through': "orm['tradeschool.Registration']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tradeschool.Venue']", 'null': 'True', 'blank': 'True'})
        },
        'tradeschool.time': {
            'Meta': {'object_name': 'Time'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tradeschool.timerange': {
            'Meta': {'object_name': 'TimeRange'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tueday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tradeschool.venue': {
            'Meta': {'object_name': 'Venue'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {'default': '20', 'max_length': '4'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#e42d4c'", 'max_length': '7'}),
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

    complete_apps = ['tradeschool']