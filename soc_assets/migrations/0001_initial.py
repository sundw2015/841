# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=64)),
                ('assets_name', models.CharField(max_length=200)),
                ('add_date', models.DateTimeField(null=True, blank=True)),
                ('last_date', models.DateTimeField(null=True, blank=True)),
                ('assets_type', models.IntegerField()),
            ],
            options={
                'db_table': 'soc_assets',
            },
        ),
    ]
