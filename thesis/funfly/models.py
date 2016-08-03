# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from moderation.db import ModeratedModel
from gm2m import GM2MField

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
    avatar = models.ImageField(upload_to='imagesandvideos/imageorvideos/avatars',
                               default='avatars/no_avatar.jpg', blank=True, null=True)
    saved_items = GM2MField()

    def __unicode__(self):
        return u'%s' % self.user


class PostComment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # post = models.ForeignKey('Youtube', related_name='comments',
    #                          verbose_name='post', on_delete=models.CASCADE)
    #

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, related_name='comments',
                             verbose_name='user', on_delete=models.CASCADE)

    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __unicode__(self):
        return u'{} @ {}'.format(self.user, self.date_added)

class Ninegag(ModeratedModel):
    title = models.CharField(max_length=100, db_index=True)
    source_url = models.CharField(max_length=200)
    imagevideo_path = models.CharField(max_length=200)
    is_video = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    nine_gag_comments = GenericRelation(PostComment, related_query_name='nine_gag_comments')

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id

    def approved_comments(self):
        return self.nine_gag_comments.filter(approved_comment=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Moderator:
        notify_user = False
        fields_exclude = ['points', 'date_added']


class Joke(ModeratedModel):
    identifier = models.CharField(max_length=50, default='', db_index=True)
    text = models.TextField(default='')
    category = models.CharField(max_length=100, null=True, blank=False, default='')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes')
    joke_comments = GenericRelation(PostComment, related_query_name='joke_comments')

    def __unicode__(self):
        return u'%s' % self.text

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id

    def approved_comments(self):
        return self.joke_comments.filter(approved_comment=True)

    def total_likes(self):
        return self.likes.count()

    def likes_users(self):
        return self.likes.all()

    class Moderator:
        notify_user = False
        fields_exclude = ['joke_comments', 'likes', 'date_added']




class Youtube(models.Model):
    identifier = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    date_added = models.DateTimeField(null=True)
    youtube_comments = GenericRelation(PostComment, related_query_name='youtube_comments')

    def __unicode__(self):
        return u'%s' % self.title

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id

    def approved_comments(self):
        return self.youtube_comments.filter(approved_comment=True)
