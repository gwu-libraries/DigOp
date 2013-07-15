# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'ui_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('startDate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('endDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('projectComplete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ui', ['Project'])

        # Adding unique constraint on 'Project', fields [u'id', 'name']
        db.create_unique(u'ui_project', [u'id', 'name'])

        # Adding model 'Item'
        db.create_table(u'ui_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ui.Project'])),
            ('barcode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('totalPages', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('itemType', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'ui', ['Item'])

        # Adding model 'ProcessingSession'
        db.create_table(u'ui_processingsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ui.Item'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('pagesDone', self.gf('django.db.models.fields.IntegerField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('operationComplete', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ui', ['ProcessingSession'])

        # Adding model 'UserProfile'
        db.create_table(u'ui_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'ui', ['UserProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'Project', fields [u'id', 'name']
        db.delete_unique(u'ui_project', [u'id', 'name'])

        # Deleting model 'Project'
        db.delete_table(u'ui_project')

        # Deleting model 'Item'
        db.delete_table(u'ui_item')

        # Deleting model 'ProcessingSession'
        db.delete_table(u'ui_processingsession')

        # Deleting model 'UserProfile'
        db.delete_table(u'ui_userprofile')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ui.item': {
            'Meta': {'object_name': 'Item'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ui.Project']"}),
            'totalPages': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'ui.processingsession': {
            'Meta': {'object_name': 'ProcessingSession'},
            'comments': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ui.Item']"}),
            'operationComplete': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pagesDone': ('django.db.models.fields.IntegerField', [], {}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'ui.project': {
            'Meta': {'unique_together': "(('id', 'name'),)", 'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'projectComplete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'ui.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['ui']