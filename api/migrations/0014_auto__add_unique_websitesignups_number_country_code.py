# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'WebsiteSignups', fields ['country_code', 'number']
        db.create_unique('api_website_singups', ['country_code', 'number'])


    def backwards(self, orm):
        # Removing unique constraint on 'WebsiteSignups', fields ['country_code', 'number']
        db.delete_unique('api_website_singups', ['country_code', 'number'])


    models = {
        'api.business': {
            'Meta': {'object_name': 'Business'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'xmpp_handle': ('django.db.models.fields.EmailField', [], {'max_length': '250'})
        },
        'api.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'api.faqs': {
            'Meta': {'object_name': 'Faqs'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'answer': ('django.db.models.fields.TextField', [], {}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Business']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'relevance': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        'api.location': {
            'Meta': {'object_name': 'Location'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'api.user': {
            'Meta': {'object_name': 'User'},
            'activate_code': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'device_token': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'gender': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'api.websitesignups': {
            'Meta': {'unique_together': "(('country_code', 'number'),)", 'object_name': 'WebsiteSignups', 'db_table': "'api_website_singups'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'default': "'91'", 'max_length': '250'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'os_type': ('django.db.models.fields.IntegerField', [], {}),
            'text_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['api']