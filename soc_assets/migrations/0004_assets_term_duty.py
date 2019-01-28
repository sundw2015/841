# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_assets', '0003_auto_20180702_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='term_duty',
            field=models.CharField(default=b'0', max_length=64),
        ),
    ]
