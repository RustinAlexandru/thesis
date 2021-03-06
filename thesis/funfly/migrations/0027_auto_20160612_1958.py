# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 16:58
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('funfly', '0026_postcomment_approved_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='post',
        ),
        migrations.AddField(
            model_name='postcomment',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
