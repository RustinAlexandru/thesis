from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'flower/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('index')}, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
