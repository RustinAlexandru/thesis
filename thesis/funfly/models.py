# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from moderation.db import ModeratedModel


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


class Ninegag(ModeratedModel):
    title = models.CharField(max_length=100)
    source_url = models.CharField(max_length=200)
    imagevideo_path = models.CharField(max_length=200)
    is_video = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Moderator:
        notify_user = False


class Joke(models.Model):
    identifier = models.CharField(max_length=50, default='')
    text = models.TextField(default='')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    category = models.CharField(max_length=100, null=True, blank=False, default='')

    def __unicode__(self):
        return u'%s' % self.text

