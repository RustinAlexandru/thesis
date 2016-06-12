# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from forms import RegisterForm
from models import Ninegag, UserProfile, Joke, Youtube, PostComment


# from youtube_parsing import youtube_search

def index(request):
    left_8_items = Ninegag.objects.order_by('-pk')[:8]
    left_6_jokes = Joke.objects.filter(category='Relationship Jokes')[:6]
    left_4_videos = Youtube.objects.order_by('-pk')[:4]
    context = {
        'items': left_8_items,
        'jokes': left_6_jokes,
        'videos': left_4_videos,
    }
    # youtube_result = youtube_search('funny')
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
            context['comments'] = PostComment.objects.filter(post_id=pk)
        return context
