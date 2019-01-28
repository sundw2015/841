# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('soc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('status', models.IntegerField(default=0)),
                ('agent_id', models.IntegerField(null=True)),
                ('crm_user_id', models.IntegerField(null=True)),
                ('crm_user_name', models.CharField(max_length=128, null=True)),
                ('license', models.CharField(max_length=128, null=True)),
                ('title', models.CharField(max_length=120, null=True)),
                ('web_title', models.CharField(default='\u4e91\u677e', max_length=120)),
                ('web_logo', models.ImageField(default='logo/logo.svg', upload_to='images/logo')),
                ('web_domain', models.CharField(max_length=256, null=True)),
                ('enable_iframe', models.BooleanField(default=True)),
                ('token', models.CharField(max_length=64, null=True)),
                ('qs_token', models.CharField(max_length=128, null=True)),
                ('qs_token_secret', models.CharField(max_length=128, null=True)),
                ('qs_api_timeout', models.IntegerField(default=60, null=True)),
                ('ssl_pub_key', models.TextField(null=True)),
                ('key', models.CharField(default=uuid.uuid4, max_length=64)),
                ('qs_api_token', models.CharField(max_length=64, null=True, blank=True)),
                ('fail_count', models.IntegerField(default=10)),
                ('fail_range_time', models.IntegerField(default=180)),
                ('fail_ban_time', models.IntegerField(default=3600)),
                ('register_time', models.IntegerField(default=180)),
                ('register_count', models.IntegerField(default=5)),
                ('register_allow', models.IntegerField(default=1)),
                ('login_allow', models.IntegerField(default=1)),
                ('login_type', models.CharField(default='username,email,phone,wechat', max_length=128)),
                ('login_timeout', models.IntegerField(default=3600)),
                ('is_find_password', models.IntegerField(default=1)),
                ('record_number', models.CharField(max_length=128, null=True, blank=True)),
                ('server_phone', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.CharField(default='', max_length=128, null=True, blank=True)),
            ],
            options={
                'db_table': 'agent',
                'verbose_name': '\u4ee3\u7406\u5546',
            },
        ),
        migrations.CreateModel(
            name='AgentPerms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'agent_perms',
                'verbose_name': '\u4ee3\u7406\u5546\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=256, null=True, blank=True)),
                ('phone', models.CharField(max_length=256, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('key', models.CharField(default=uuid.uuid4, max_length=64)),
                ('qs_api_token', models.CharField(max_length=64, null=True, blank=True)),
                ('type', models.IntegerField(default=0)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'company',
                'verbose_name': '\u516c\u53f8\u5ba2\u6237',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('type', models.IntegerField()),
                ('priority', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
                'verbose_name': '\u6d88\u606f',
            },
        ),
        migrations.CreateModel(
            name='Perms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('perms_id', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'db_table': 'perms',
                'verbose_name': '\u6a21\u5757\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='SocLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=128)),
                ('level', models.CharField(max_length=128)),
                ('info', models.CharField(max_length=128)),
                ('role', models.CharField(default='', max_length=64, null=True)),
                ('logtype', models.IntegerField(blank=True, null=True, choices=[(1, '\u64cd\u4f5c\u65e5\u5fd7'), (2, '\u767b\u9646\u65e5\u5fd7'), (3, '\u6ce8\u518c\u65e5\u5fd7')])),
                ('login_status', models.IntegerField(blank=True, null=True, choices=[(1, '\u767b\u9646\u6210\u529f'), (2, '\u767b\u9646\u5931\u8d25')])),
                ('ip', models.CharField(max_length=32, null=True, blank=True)),
                ('url', models.CharField(default='', max_length=256, null=True, blank=True)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'soc_log',
                'verbose_name': 'soc\u65e5\u5fd7',
            },
        ),
        migrations.AddField(
            model_name='agentperms',
            name='perms',
            field=models.ForeignKey(to='soc.Perms'),
        ),
        migrations.AlterUniqueTogether(
            name='agentperms',
            unique_together=set([('agent', 'perms')]),
        ),
    ]
