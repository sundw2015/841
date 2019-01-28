# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assets_type_name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'soc_assets_type',
            },
        ),
    ]
