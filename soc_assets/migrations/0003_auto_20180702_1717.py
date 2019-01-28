# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_assets', '0002_assetstype'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_group_id', models.CharField(default=0, max_length=64)),
                ('term_group_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'soc_term_group',
            },
        ),
        migrations.AddField(
            model_name='assets',
            name='term_group_id',
            field=models.CharField(default=b'0', max_length=64),
        ),
    ]
