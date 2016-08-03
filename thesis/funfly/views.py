# -*- coding: utf-8 -*-
import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.list import ListView
from el_pagination.views import AjaxListView

from forms import RegisterForm, CommentForm, AddItemForm
from models import Ninegag, UserProfile, Joke, Youtube, PostComment

from django.http import HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.apps import apps
import json
import ast


# from youtube_parsing import youtube_search
from thesis.settings import MEDIA_ROOT


def anonymous_required(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect('index')
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)


def index(request):
    left_8_items = Ninegag.objects.order_by('-pk')[:8]
    left_6_jokes = Joke.objects.order_by('-pk')[:6]
    left_4_videos = Youtube.objects.order_by('-pk')[:4]
    context = {
        'items': left_8_items,
        'jokes': left_6_jokes,
        'videos': left_4_videos,
    }
    user = request.user
    if user.is_authenticated():
        user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST' and request.is_ajax():
        data_sent = {
        }
        item_info = json.loads(request.POST['data'])
        if item_info["item_type"] == 'Ninegag':
            item = Ninegag.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Youtube':
            item = Youtube.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Joke':
            item = Joke.objects.get(pk=item_info["item_id"])

        try:
            user_profile.saved_items.add(item)
        except IntegrityError as integrity_error:
            data_sent["integrity_error"] = integrity_error.__class__.__name__

        return JsonResponse(data_sent)

    return render(request, 'funfly/layout.html', context)


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {
            'RegisterForm': form
        }
        return render(request, 'funfly/register.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            if form.cleaned_data['sex']:
                sex = form.cleaned_data["sex"]
            else:
                sex = None
            if form.cleaned_data['city']:
                city = form.cleaned_data["city"]
            else:
                city = None
            if form.cleaned_data['timezone']:
                timezone = form.cleaned_data["timezone"]
            else:
                timezone = None
            if form.cleaned_data['avatar']:
                avatar = form.cleaned_data['avatar']
                avatar = form.resize_avatar()
            else:
                avatar = None


            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()


            profile = UserProfile.objects.create(user=user, sex=sex, city=city, timezone=timezone, avatar=avatar)

            user_auth = authenticate(username=username, password=password)

            if user_auth is None:
                return redirect('login')
            else:
                login(request, user_auth)
                return redirect('index')
        else:
            context = {
                'RegisterForm': form
            }
            return render(request, 'funfly/register.html', context)


def about(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'funfly/about.html', context)


class ViewProfile(DetailView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super(ViewProfile, self).get_context_data(**kwargs)
        context['username'] = context['object'].user.username
        return context

class VideoPostDetails(DetailView):
    model = Youtube

    def get_context_data(self, **kwargs):
        context = super(VideoPostDetails, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            # context['comments'] = PostComment.objects.filter(content_type__postcomment__object_id=pk)
            comments = Youtube.objects.get(pk=pk).youtube_comments.all()
            context['comments'] = comments
        context['CommentForm'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            message = form.cleaned_data['text']
            pk = self.kwargs['pk']
            user = self.request.user
            youtube_post = Youtube.objects.get(pk=pk)
            PostComment.objects.create(text=message, content_object=youtube_post, user=user)
            return redirect(reverse('video_post_details', kwargs={'pk': pk}))
        else:
            return redirect(reverse('video_post_details', kwargs={'pk': self.kwargs['pk']}))


class JokePostDetails(DetailView):
    model = Joke

    def get_context_data(self, **kwargs):
        context = super(JokePostDetails, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            # context['comments'] = PostComment.objects.filter(content_type__postcomment__object_id=pk)
            comments = Joke.objects.get(pk=pk).joke_comments.all()
            context['comments'] = comments
        context['CommentForm'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            message = form.cleaned_data['text']
            pk = self.kwargs['pk']
            user = self.request.user
            joke_post = Joke.objects.get(pk=pk)
            PostComment.objects.create(text=message, content_object=joke_post, user=user)
            return redirect(reverse('joke_post_details', kwargs={'pk': pk}))
        else:
            return redirect(reverse('joke_post_details', kwargs={'pk': self.kwargs['pk']}))


class NinegagPostDetails(DetailView):
    model = Ninegag

    def get_context_data(self, **kwargs):
        context = super(NinegagPostDetails, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            # context['comments'] = PostComment.objects.filter(content_type__postcomment__object_id=pk)
            comments = Ninegag.objects.get(pk=pk).nine_gag_comments.all()
            context['comments'] = comments
        context['CommentForm'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            message = form.cleaned_data['text']
            pk = self.kwargs['pk']
            user = self.request.user
            ninegag_post = Ninegag.objects.get(pk=pk)
            PostComment.objects.create(text=message, content_object=ninegag_post, user=user)
            return redirect(reverse('ninegag_post_details', kwargs={'pk': pk}))
        else:
            return redirect(reverse('ninegag_post_details', kwargs={'pk': self.kwargs['pk']}))


class VideosList(AjaxListView):
    model = Youtube
    context_object_name = 'videos'
    template_name = 'videos.html'
    page_template = 'videos_list.html'

    def get_queryset(self):
        if self.request.is_ajax():
            date_orderby_val = self.request.GET.get("date_orderBy")
            title_orderby_val = self.request.GET.get("title_orderBy")

            if date_orderby_val is None:
                return Youtube.objects.order_by(title_orderby_val)
            elif title_orderby_val is None:
                return Youtube.objects.order_by(date_orderby_val)
        else:                                   # normal get request
            return Youtube.objects.all()



class NinegagsList(AjaxListView):
    model = Ninegag
    context_object_name = 'ninegags'
    template_name = 'ninegags.html'
    page_template = 'ninegags_ajax.html'



    def get_queryset(self):
        if self.request.is_ajax():
            filter_val = self.request.GET.get("itemType")
            date_orderby_val = self.request.GET.get("date_orderBy")
            points_orderby_val = self.request.GET.get("points_orderBy")
            if filter_val != 'Any' and filter_val is not None:
                filter_val = ast.literal_eval(filter_val)  # String "False" -> bool False
                new_context = Ninegag.objects.filter(is_video=filter_val).order_by(date_orderby_val, points_orderby_val)
            elif filter_val == 'Any':
                new_context = Ninegag.objects.order_by(date_orderby_val, points_orderby_val)
            return Ninegag.objects.all()
        else:                                   # normal get request
            return Ninegag.objects.all()


    def get_template_names(self):
        if self.request.is_ajax():
            return ['ninegags_ajax.html']
        else:
            return ['ninegags.html']


class JokesList(AjaxListView):
    model = Joke
    context_object_name = 'jokes'
    template_name = 'jokes.html'
    page_template = 'joke_list.html'

    def get_queryset(self):
        if self.request.is_ajax():
            filter_val = self.request.GET.get("joke_category")
            date_orderby_val = self.request.GET.get("date_orderBy")
            likes_orderby_val = self.request.GET.get("likes_orderBy")
            dislikes_orderby_val = self.request.GET.get("dislikes_orderBy")

            if (filter_val == 'Any' or filter_val is None) and \
                    date_orderby_val is None and likes_orderby_val is None and dislikes_orderby_val is None:
                new_context = Joke.objects.all()
            elif filter_val == 'Any' and date_orderby_val is None:
                new_context = Joke.objects.order_by(likes_orderby_val, dislikes_orderby_val)
            elif filter_val == 'Any' and likes_orderby_val is None:
                new_context = Joke.objects.order_by(date_orderby_val, dislikes_orderby_val)
            elif filter_val == 'Any' and dislikes_orderby_val is None:
                new_context = Joke.objects.order_by(date_orderby_val, likes_orderby_val)
            elif filter_val == 'Any':
                new_context = Joke.objects.order_by(date_orderby_val, likes_orderby_val, dislikes_orderby_val)
            elif date_orderby_val is None and likes_orderby_val is None and dislikes_orderby_val is None:
                new_context = Joke.objects.filter(category=filter_val)
            elif date_orderby_val is None:
                new_context = Joke.objects.filter(category=filter_val).order_by(likes_orderby_val, dislikes_orderby_val)
            elif likes_orderby_val is None:
                new_context = Joke.objects.filter(category=filter_val).order_by(date_orderby_val, dislikes_orderby_val)
            elif dislikes_orderby_val is None:
                new_context = Joke.objects.filter(category=filter_val).order_by(date_orderby_val, likes_orderby_val)
            else:
                new_context = Joke.objects.filter(category=filter_val).order_by(date_orderby_val, likes_orderby_val, dislikes_orderby_val)
            return new_context

        else:  # normal get request
            return Joke.objects.all()

    def get_context_data(self, **kwargs):
        context = super(JokesList, self).get_context_data(**kwargs)
        categories = Joke.objects.values('category')
        categories_list = sorted(set(map(lambda d: d['category'], categories)))
        context['categories'] = categories_list
        return context

@login_required
def add_item_to_savelist(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST' and request.is_ajax():
        data_sent = {
        }
        item_info = json.loads(request.POST['data'])
        if item_info["item_type"] == 'Ninegag':
            item = Ninegag.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Youtube':
            item = Youtube.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Joke':
            item = Joke.objects.get(pk=item_info["item_id"])

        try:
            user_profile.saved_items.add(item)
        except IntegrityError as integrity_error:
            data_sent["integrity_error"] = integrity_error.__class__.__name__

        return JsonResponse(data_sent)

@login_required
def like_item(request):
    user = request.user
    if request.method == 'POST' and request.is_ajax():
        data_sent = {
        }
        item_info = json.loads(request.POST['data'])
        if item_info["item_type"] == 'Ninegag':
            item = Ninegag.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Youtube':
            item = Youtube.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Joke':
            item = Joke.objects.get(pk=item_info["item_id"])
            if item.likes.filter(id=user.id).exists():
                item.likes.remove(user)
                message = 'You disliked this'
            else:
                item.likes.add(user)
            data_sent['likes'] = item.total_likes()
            names = list(item.likes_users().values('username'))
            data_sent['likes_list'] = names

        return JsonResponse(data_sent)

@login_required
def add_point(request):
    if request.method == 'POST' and request.is_ajax():
        data_sent = {
        }
        item_info = json.loads(request.POST['data'])
        if item_info["item_type"] == 'Ninegag':
            item = Ninegag.objects.get(pk=item_info["item_id"])
            item.points += 1
            item.save()
            data_sent['points'] = item.points
            button = 'add_button_' + item_info["item_id"]

        if item_info["item_type"] == 'Youtube':
            item = Youtube.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Joke':
            item = Joke.objects.get(pk=item_info["item_id"])

        return JsonResponse(data_sent)


@login_required
def comment_approve(request, pk):
    comment = PostComment.objects.get(pk=pk)
    if request.user.has_perm('Can change post comment'):
        comment.approve()
    if comment.content_type.model == 'joke':
        return redirect('joke_post_details', pk=comment.object_id)
    elif comment.content_type.model == 'ninegag':
        return redirect('ninegag_post_details', pk=comment.object_id)
    return redirect('video_post_details', pk=comment.object_id)


@login_required
def comment_remove(request, pk):
    comment = PostComment.objects.get(pk=pk)
    post_pk = comment.object_id
    if request.user.has_perm(('Can change post comment')):
        comment.delete()
    if comment.content_type.model == 'joke':
        return redirect('joke_post_details', pk=comment.object_id)
    elif comment.content_type.model == 'ninegag':
        return redirect('ninegag_post_details', pk=comment.object_id)
    return redirect('video_post_details', pk=post_pk)


def save_file(_file, path=''):
    filename = _file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    path = '{0}/{1}'.format('funfly/imagesandvideos/imageorvideos/', str(filename))
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return path


def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()


@user_passes_test(is_moderator)
def add_item(request):
    context = {}
    if request.method == 'GET':
        form = AddItemForm()
        context = {
            'AddItemForm': form,
        }
        return render(request, 'funfly/add_item.html', context)
    elif request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item_option = form.cleaned_data['item_type']
            if item_option == 'Ninegag':
                title = form.cleaned_data['title']
                url = form.cleaned_data['url']
                imagevideo = request.FILES['media']
                path = save_file(imagevideo)
                file_path, file_extension = os.path.splitext(path)
                if file_extension == '.png' or file_extension == '.jpg':
                    is_video = False
                else:
                    is_video = True
                ninegag = Ninegag.objects.create(title=title, source_url=url, imagevideo_path=path, is_video=is_video)
            elif item_option == 'Video':
                pass
            else:
                pass
            return redirect('add_item')
        else:
            context = {
                'AddItemForm': form
            }
            return render(request, 'funfly/add_item.html', context)


@login_required
def saved_items_list(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'GET':
        if request.is_ajax():
            item_type = request.GET.get('itemType')
            if item_type == 'Any':
                saved_items = user_profile.saved_items.all()
                context = {
                    'saved_items': saved_items
                }
                return render(request, 'funfly/saved_items_list_ajax.html', context)
            else:
                model_type = apps.get_model('funfly', request.GET.get('itemType'))
                saved_items = user_profile.saved_items.filter(Model=model_type)
                context = {
                    'saved_items' : saved_items
                }
                return render(request, 'funfly/saved_items_list_ajax.html', context)

        saved_items = user_profile.saved_items.all()
        context = {
            'saved_items': saved_items
        }
        return render(request, 'funfly/saved_items_list.html', context)
    elif request.method == 'POST' and request.is_ajax():
        context = {}
        item_info = json.loads(request.POST['data'])
        if item_info["item_type"] == 'Ninegag':
            item = Ninegag.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Youtube':
            item = Youtube.objects.get(pk=item_info["item_id"])

        if item_info["item_type"] == 'Joke':
            item = Joke.objects.get(pk=item_info["item_id"])

        user_profile.saved_items.remove(item)
        saved_items = user_profile.saved_items.all()
        context = {
            'saved_items': saved_items
        }
        return render_to_response('funfly/saved_items_list.html',context=context)
        # return render(request,'funfly/saved_items_list.html', context)

