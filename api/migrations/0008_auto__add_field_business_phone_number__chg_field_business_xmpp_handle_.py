# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Business.phone_number'
        db.add_column('api_business', 'phone_number',
                      self.gf('django.db.models.fields.CharField')(default='1234567890', max_length=250),
                      keep_default=False)


        # Changing field 'Business.xmpp_handle'
        db.alter_column('api_business', 'xmpp_handle', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Business.email'
        db.alter_column('api_business', 'email', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

    def backwards(self, orm):
        # Deleting field 'Business.phone_number'
        db.delete_column('api_business', 'phone_number')


        # Changing field 'Business.xmpp_handle'
        db.alter_column('api_business', 'xmpp_handle', self.gf('django.db.models.fields.EmailField')(max_length=250))

        # Changing field 'Business.email'
        db.alter_column('api_business', 'email', self.gf('django.db.models.fields.EmailField')(max_length=250, null=True))

    models = {
        'api.business': {
            'Meta': {'object_name': 'Business'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'xmpp_handle': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'api.faqs': {
            'Meta': {'object_name': 'Faqs'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'answer': ('django.db.models.fields.TextField', [], {}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Business']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'api.favourite': {
            'Meta': {'object_name': 'Favourite'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Business']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.User']"})
        },
        'api.user': {
            'Meta': {'object_name': 'User'},
            'activate_code': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device_token': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['api']