# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FernandUser'
        db.create_table(u'people_fernanduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('alternate_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('structure_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email_invalid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('state_or_province', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('country_id', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('phone_mobile', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('phone_alternate', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('language_id', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('birthday', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('place_of_birth', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('national_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('id_card_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('sis_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('vat', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('rc', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'people', ['FernandUser'])

        # Adding M2M table for field groups on 'FernandUser'
        m2m_table_name = db.shorten_name(u'people_fernanduser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fernanduser', models.ForeignKey(orm[u'people.fernanduser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fernanduser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'FernandUser'
        m2m_table_name = db.shorten_name(u'people_fernanduser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fernanduser', models.ForeignKey(orm[u'people.fernanduser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fernanduser_id', 'permission_id'])

        # Adding model 'PasswordReset'
        db.create_table(u'people_passwordreset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.FernandUser'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'people', ['PasswordReset'])


    def backwards(self, orm):
        # Deleting model 'FernandUser'
        db.delete_table(u'people_fernanduser')

        # Removing M2M table for field groups on 'FernandUser'
        db.delete_table(db.shorten_name(u'people_fernanduser_groups'))

        # Removing M2M table for field user_permissions on 'FernandUser'
        db.delete_table(db.shorten_name(u'people_fernanduser_user_permissions'))

        # Deleting model 'PasswordReset'
        db.delete_table(u'people_passwordreset')


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
        u'people.fernanduser': {
            'Meta': {'object_name': 'FernandUser'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'alternate_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'country_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'email_invalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_card_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'language_id': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'national_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone_alternate': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'place_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'rc': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'sis_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'state_or_province': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'structure_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'vat': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'people.passwordreset': {
            'Meta': {'object_name': 'PasswordReset'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.FernandUser']"})
        }
    }

    complete_apps = ['people']