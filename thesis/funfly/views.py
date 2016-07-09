# -*- coding: utf-8 -*-
import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.list import ListView
from el_pagination.views import AjaxListView

from forms import RegisterForm, CommentForm, AddItemForm
from models import Ninegag, UserProfile, Joke, Youtube, PostComment

from django.http import HttpResponseNotAllowed, HttpResponseRedirect

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
    return render(request, 'funfly/layout.html', context)

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {
            'RegisterForm': form
        }
        return render(request, 'funfly/register.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            sex = form.cleaned_data["sex"]
            city = form.cleaned_data["city"]
            timezone = form.cleaned_data["timezone"]

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            profile = UserProfile.objects.create(user=user, sex=sex, city=city, timezone=timezone)

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

class VideosList(ListView):
    model = Youtube
    context_object_name = 'videos'
    paginate_by = 5


class NinegagsList(ListView):
    model = Ninegag
    context_object_name = 'ninegags'
    paginate_by = 5

class JokesList(AjaxListView):
    model = Joke
    context_object_name = 'jokes'
    template_name = 'jokes.html'
    page_template = 'joke_list.html'

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

def save_file(file, path=''):
    filename = file._get_name()
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
    # elif request.method == 'POST':
    #     form = AddItemForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         item_option = form.cleaned_data['item_type']
    #         if item_option == 'Ninegag':
    #             title = form.cleaned_data['title']
    #             url = form.cleaned_data['url']
    #             imagevideo = request.FILES['media']
    #             path = save_file(imagevideo)
    #             file_path, file_extension = os.path.splitext(path)
    #             if file_extension == '.png' or file_extension == '.jpg':
    #                 is_video = False
    #             else:
    #                 is_video = True
    #             ninegag = Ninegag.objects.create(title=title, source_url=url, imagevideo_path=path, is_video=is_video)
    #         elif item_option == 'Video':
    #             pass
    #         else:
    #             pass
    #         return redirect('add_item')
    #     else:
    #         context = {
    #             'AddItemForm': form
    #         }
    #         return render(request, 'funfly/add_item.html', context)



