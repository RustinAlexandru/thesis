import urllib2
from StringIO import StringIO

import pytz
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from io import BytesIO
from PIL import Image as pil
import StringIO


from funfly.models import UserProfile


class TimezoneMiddleware(object):

    def process_request(self, request):
        pass
        if request.user.is_authenticated() and request.user.userprofile.timezone:
            timezone.activate(pytz.timezone(request.user.userprofile.timezone))
        else:
            timezone.deactivate()


def resize_avatar(file, name):
        img = pil.open(file)

        img.thumbnail((75, 75), pil.ANTIALIAS)

        thumb_io = StringIO.StringIO()
        img.save(thumb_io, 'JPEG')

        filename = name

        file = InMemoryUploadedFile(thumb_io,
                                    u"avatar",
                                    filename,
                                    '.JPG',
                                    thumb_io.len,
                                    None)

        return file




def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        sex = response.get('gender')
        city = response.get('location')['name']
        picture = response.get('picture')
        photo_url = "http://graph.facebook.com/%s/picture?type=large" \
                    % response['id']
        request = urllib2.Request(photo_url)
        photo_response = urllib2.urlopen(request).read()
        io = BytesIO(photo_response)
        photo = File(io)
        photo = resize_avatar(photo, 'profile_pic_{}'.format(response['id']))
        if sex == 'male':
            sex = '1'
        else:       # female
            sex = '0'
        # profile_timezone = response.get('timezone')

        try:
            user_profile = UserProfile.objects.get(user=user)
            user_profile.sex = sex
            user_profile.city = city
            user_profile.avatar.save('profile_pic_{}.jpg'.format(response['id']), photo)
            # profile.timezone = profile_timezone
            user_profile.save()
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user, sex=sex, city=city)
            profile.sex = sex
            profile.city = city
            profile.avatar.save('profile_pic_{}.jpg'.format(response['id']), photo)
            # profile.timezone = profile_timezone
            profile.save()
