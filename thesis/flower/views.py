# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from forms import RegisterForm
from wiki import get_wiki_html


def index(request):
    context = {}
    wiki_page = get_wiki_html()

    context = {
        'wiki': wiki_page,
    }
    return render(request, 'flower/index.html', context)


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {
            'RegisterForm': form
        }
        return render(request, 'flower/register.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            user_auth = authenticate(username=username, password=password)

            if user_auth is None:
                return redirect('login')
            else:
                login(request, user_auth)
        else:
            context = {
                'RegisterForm': form
            }
            return render(request, 'flower/register.html', context)
