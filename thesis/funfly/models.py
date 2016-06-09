# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
SEX = (
    ('0', 'Female'),
    ('1', 'Male'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    sex = models.CharField(null=True, max_length=1, default=None, choices=SEX,
        verbose_name=u'Are you male or female?')
    city = models.CharField(null=True, default=None, max_length=100)
    timezone = models.CharField(null=True, default=None, max_length=100)

    def __unicode__(self):
        return u'%s' % self.user


class Ninegag(models.Model):
    title = models.CharField(max_length=100)
    source_url = models.CharField(max_length=200)
    imagevideo_path = models.CharField(max_length=200)
    is_video = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title


class Joke(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.title

