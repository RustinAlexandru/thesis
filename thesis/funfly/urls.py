from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from forms import CustomAuthenticationForm
from funfly.views import VideoPostDetails
from . import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/$', auth_views.login, {
                      'template_name': 'funfly/login.html',
                      'authentication_form': CustomAuthenticationForm
                      }, name='login'),
                  url(r'^logout/$', auth_views.logout,
                      {'next_page': reverse_lazy('index')}, name='logout'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^$', views.index, name='index'),
                  url(r'^video_post/(?P<pk>\d+)/$', VideoPostDetails.as_view(template_name='video_post.html'),
                      name='video_post_details'),
                  url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
                  url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
