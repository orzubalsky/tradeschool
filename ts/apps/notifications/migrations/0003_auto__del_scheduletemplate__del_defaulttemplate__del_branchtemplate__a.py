# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ScheduleTemplate'
        db.delete_table('notifications_scheduletemplate')

        # Deleting model 'DefaultTemplate'
        db.delete_table('notifications_defaulttemplate')

        # Deleting model 'BranchTemplate'
        db.delete_table('notifications_branchtemplate')

        # Adding model 'DefaultEmailContainer'
        db.create_table('notifications_defaultemailcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.StudentConfirmation'])),
            ('student_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.StudentReminder'])),
            ('student_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.StudentFeedback'])),
            ('teacher_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherConfirmation'])),
            ('teacher_class_approval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherClassApproval'])),
            ('teacher_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherReminder'])),
            ('teacher_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherFeedback'])),
        ))
        db.send_create_signal('notifications', ['DefaultEmailContainer'])

        # Adding model 'BranchEmailContainer'
        db.create_table('notifications_branchemailcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.StudentConfirmation'])),
            ('student_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.StudentReminder'])),
            ('student_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.StudentFeedback'])),
            ('teacher_confirmation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherConfirmation'])),
            ('teacher_class_approval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherClassApproval'])),
            ('teacher_reminder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherReminder'])),
            ('teacher_feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.TeacherFeedback'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails', to=orm['tradeschool.Branch'])),
        ))
        db.send_create_signal('notifications', ['BranchEmailContainer'])

        # Adding field 'ScheduleEmailContainer.student_confirmation'
        db.add_column('notifications_scheduleemailcontainer', 'student_confirmation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.StudentConfirmation']),
                      keep_default=False)

        # Adding field 'ScheduleEmailContainer.student_reminder'
        db.add_column('notifications_scheduleemailcontainer', 'student_reminder',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.StudentReminder']),
                      keep_default=False)

        # Adding field 'ScheduleEmailContainer.student_feedback'
        db.add_column('notifications_scheduleemailcontainer', 'student_feedback',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.StudentFeedback']),
                      keep_default=False)

        # Adding field 'ScheduleEmailContainer.teacher_confirmation'
        db.add_column('notifications_scheduleemailcontainer', 'teacher_confirmation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.TeacherConfirmation']),
                      keep_default=False)

        # Adding field 'ScheduleEmailContainer.teacher_class_approval'
        db.add_column('notifications_scheduleemailcontainer', 'teacher_class_approval',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.TeacherClassApproval']),
                      keep_default=False)

        # Adding field 'ScheduleEmailContainer.teacher_reminder'
        db.add_column('notifications_scheduleemailcontainer', 'teacher_reminder',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.TeacherReminder']),
                      keep_default=False)

        # Adding field 'ScheduleEmailContainer.teacher_feedback'
        db.add_column('notifications_scheduleemailcontainer', 'teacher_feedback',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.TeacherFeedback']),
                      keep_default=False)

        # Deleting field 'StudentFeedback.container'
        db.delete_column('notifications_studentfeedback', 'container_id')

        # Deleting field 'StudentFeedback.template'
        db.delete_column('notifications_studentfeedback', 'template_id')

        # Adding field 'StudentFeedback.subject'
        db.add_column('notifications_studentfeedback', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'StudentFeedback.content'
        db.add_column('notifications_studentfeedback', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Deleting field 'StudentReminder.container'
        db.delete_column('notifications_studentreminder', 'container_id')

        # Deleting field 'StudentReminder.template'
        db.delete_column('notifications_studentreminder', 'template_id')

        # Adding field 'StudentReminder.subject'
        db.add_column('notifications_studentreminder', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'StudentReminder.content'
        db.add_column('notifications_studentreminder', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Deleting field 'TeacherClassApproval.container'
        db.delete_column('notifications_teacherclassapproval', 'container_id')

        # Deleting field 'TeacherClassApproval.template'
        db.delete_column('notifications_teacherclassapproval', 'template_id')

        # Adding field 'TeacherClassApproval.subject'
        db.add_column('notifications_teacherclassapproval', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'TeacherClassApproval.content'
        db.add_column('notifications_teacherclassapproval', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Deleting field 'TeacherConfirmation.container'
        db.delete_column('notifications_teacherconfirmation', 'container_id')

        # Deleting field 'TeacherConfirmation.template'
        db.delete_column('notifications_teacherconfirmation', 'template_id')

        # Adding field 'TeacherConfirmation.subject'
        db.add_column('notifications_teacherconfirmation', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'TeacherConfirmation.content'
        db.add_column('notifications_teacherconfirmation', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Deleting field 'TeacherReminder.container'
        db.delete_column('notifications_teacherreminder', 'container_id')

        # Deleting field 'TeacherReminder.template'
        db.delete_column('notifications_teacherreminder', 'template_id')

        # Adding field 'TeacherReminder.subject'
        db.add_column('notifications_teacherreminder', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'TeacherReminder.content'
        db.add_column('notifications_teacherreminder', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Deleting field 'TeacherFeedback.container'
        db.delete_column('notifications_teacherfeedback', 'container_id')

        # Deleting field 'TeacherFeedback.template'
        db.delete_column('notifications_teacherfeedback', 'template_id')

        # Adding field 'TeacherFeedback.subject'
        db.add_column('notifications_teacherfeedback', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'TeacherFeedback.content'
        db.add_column('notifications_teacherfeedback', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Deleting field 'StudentConfirmation.container'
        db.delete_column('notifications_studentconfirmation', 'container_id')

        # Deleting field 'StudentConfirmation.template'
        db.delete_column('notifications_studentconfirmation', 'template_id')

        # Adding field 'StudentConfirmation.subject'
        db.add_column('notifications_studentconfirmation', 'subject',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=140),
                      keep_default=False)

        # Adding field 'StudentConfirmation.content'
        db.add_column('notifications_studentconfirmation', 'content',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ScheduleTemplate'
        db.create_table('notifications_scheduletemplate', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.BranchTemplate'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('notifications', ['ScheduleTemplate'])

        # Adding model 'DefaultTemplate'
        db.create_table('notifications_defaulttemplate', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('notifications', ['DefaultTemplate'])

        # Adding model 'BranchTemplate'
        db.create_table('notifications_branchtemplate', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.DefaultTemplate'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['tradeschool.Branch'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('notifications', ['BranchTemplate'])

        # Deleting model 'DefaultEmailContainer'
        db.delete_table('notifications_defaultemailcontainer')

        # Deleting model 'BranchEmailContainer'
        db.delete_table('notifications_branchemailcontainer')

        # Deleting field 'ScheduleEmailContainer.student_confirmation'
        db.delete_column('notifications_scheduleemailcontainer', 'student_confirmation_id')

        # Deleting field 'ScheduleEmailContainer.student_reminder'
        db.delete_column('notifications_scheduleemailcontainer', 'student_reminder_id')

        # Deleting field 'ScheduleEmailContainer.student_feedback'
        db.delete_column('notifications_scheduleemailcontainer', 'student_feedback_id')

        # Deleting field 'ScheduleEmailContainer.teacher_confirmation'
        db.delete_column('notifications_scheduleemailcontainer', 'teacher_confirmation_id')

        # Deleting field 'ScheduleEmailContainer.teacher_class_approval'
        db.delete_column('notifications_scheduleemailcontainer', 'teacher_class_approval_id')

        # Deleting field 'ScheduleEmailContainer.teacher_reminder'
        db.delete_column('notifications_scheduleemailcontainer', 'teacher_reminder_id')

        # Deleting field 'ScheduleEmailContainer.teacher_feedback'
        db.delete_column('notifications_scheduleemailcontainer', 'teacher_feedback_id')

        # Adding field 'StudentFeedback.container'
        db.add_column('notifications_studentfeedback', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'StudentFeedback.template'
        db.add_column('notifications_studentfeedback', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'StudentFeedback.subject'
        db.delete_column('notifications_studentfeedback', 'subject')

        # Deleting field 'StudentFeedback.content'
        db.delete_column('notifications_studentfeedback', 'content')

        # Adding field 'StudentReminder.container'
        db.add_column('notifications_studentreminder', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'StudentReminder.template'
        db.add_column('notifications_studentreminder', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'StudentReminder.subject'
        db.delete_column('notifications_studentreminder', 'subject')

        # Deleting field 'StudentReminder.content'
        db.delete_column('notifications_studentreminder', 'content')

        # Adding field 'TeacherClassApproval.container'
        db.add_column('notifications_teacherclassapproval', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'TeacherClassApproval.template'
        db.add_column('notifications_teacherclassapproval', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'TeacherClassApproval.subject'
        db.delete_column('notifications_teacherclassapproval', 'subject')

        # Deleting field 'TeacherClassApproval.content'
        db.delete_column('notifications_teacherclassapproval', 'content')

        # Adding field 'TeacherConfirmation.container'
        db.add_column('notifications_teacherconfirmation', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'TeacherConfirmation.template'
        db.add_column('notifications_teacherconfirmation', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'TeacherConfirmation.subject'
        db.delete_column('notifications_teacherconfirmation', 'subject')

        # Deleting field 'TeacherConfirmation.content'
        db.delete_column('notifications_teacherconfirmation', 'content')

        # Adding field 'TeacherReminder.container'
        db.add_column('notifications_teacherreminder', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'TeacherReminder.template'
        db.add_column('notifications_teacherreminder', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'TeacherReminder.subject'
        db.delete_column('notifications_teacherreminder', 'subject')

        # Deleting field 'TeacherReminder.content'
        db.delete_column('notifications_teacherreminder', 'content')

        # Adding field 'TeacherFeedback.container'
        db.add_column('notifications_teacherfeedback', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'TeacherFeedback.template'
        db.add_column('notifications_teacherfeedback', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'TeacherFeedback.subject'
        db.delete_column('notifications_teacherfeedback', 'subject')

        # Deleting field 'TeacherFeedback.content'
        db.delete_column('notifications_teacherfeedback', 'content')

        # Adding field 'StudentConfirmation.container'
        db.add_column('notifications_studentconfirmation', 'container',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleEmailContainer']),
                      keep_default=False)

        # Adding field 'StudentConfirmation.template'
        db.add_column('notifications_studentconfirmation', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.ScheduleTemplate']),
                      keep_default=False)

        # Deleting field 'StudentConfirmation.subject'
        db.delete_column('notifications_studentconfirmation', 'subject')

        # Deleting field 'StudentConfirmation.content'
        db.delete_column('notifications_studentconfirmation', 'content')


    models = {
        'notifications.branchemailcontainer': {
            'Meta': {'object_name': 'BranchEmailContainer'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['tradeschool.Branch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'student_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentConfirmation']"}),
            'student_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentFeedback']"}),
            'student_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentReminder']"}),
            'teacher_class_approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherClassApproval']"}),
            'teacher_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherConfirmation']"}),
            'teacher_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherFeedback']"}),
            'teacher_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherReminder']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.defaultemailcontainer': {
            'Meta': {'object_name': 'DefaultEmailContainer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'student_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentConfirmation']"}),
            'student_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentFeedback']"}),
            'student_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentReminder']"}),
            'teacher_class_approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherClassApproval']"}),
            'teacher_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherConfirmation']"}),
            'teacher_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherFeedback']"}),
            'teacher_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherReminder']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.scheduleemailcontainer': {
            'Meta': {'object_name': 'ScheduleEmailContainer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['tradeschool.Schedule']"}),
            'student_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentConfirmation']"}),
            'student_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentFeedback']"}),
            'student_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.StudentReminder']"}),
            'teacher_class_approval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherClassApproval']"}),
            'teacher_confirmation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherConfirmation']"}),
            'teacher_feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherFeedback']"}),
            'teacher_reminder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.TeacherReminder']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.studentconfirmation': {
            'Meta': {'object_name': 'StudentConfirmation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.studentfeedback': {
            'Meta': {'object_name': 'StudentFeedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.studentreminder': {
            'Meta': {'object_name': 'StudentReminder'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherclassapproval': {
            'Meta': {'object_name': 'TeacherClassApproval'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherconfirmation': {
            'Meta': {'object_name': 'TeacherConfirmation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherfeedback': {
            'Meta': {'object_name': 'TeacherFeedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'notifications.teacherreminder': {
            'Meta': {'object_name': 'TeacherReminder'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
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
            'category': ('django.db.models.fields.SmallIntegerField', [], {'default': '6', 'max_length': '1'}),
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
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'0f4fd8785cea11e282640023dffd8312'", 'unique': 'True', 'max_length': '32'}),
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
            'hashcode': ('django.db.models.fields.CharField', [], {'default': "'0f5186025cea11e2a21c0023dffd8312'", 'unique': 'True', 'max_length': '32'}),
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
            'color': ('django.db.models.fields.CharField', [], {'default': "'#231c9d'", 'max_length': '7'}),
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