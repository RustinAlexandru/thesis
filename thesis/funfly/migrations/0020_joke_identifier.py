# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funfly', '0019_joke_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='joke',
            name='identifier',
            field=models.CharField(default='', max_length=50),
        ),
    ]
