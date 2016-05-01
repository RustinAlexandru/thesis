from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

from forms import CustomAuthenticationForm
from . import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/$', 'django.contrib.auth.views.login', {
                      'template_name': 'flower/login.html',
                      'authentication_form': CustomAuthenticationForm
                      }, name='login'),
                  url(r'^logout/$', 'django.contrib.auth.views.logout',
                      {'next_page': reverse_lazy('index')}, name='logout'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^$', views.index, name='index'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
