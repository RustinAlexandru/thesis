# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('funfly', '0025_auto_20160612_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='approved_comment',
            field=models.BooleanField(default=False),
        ),
    ]
