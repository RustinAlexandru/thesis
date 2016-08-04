import pytz
from django.utils import timezone

from funfly.models import UserProfile


class TimezoneMiddleware(object):

    def process_request(self, request):
        pass
        if request.user.is_authenticated() and request.user.userprofile.timezone:
            timezone.activate(pytz.timezone(request.user.userprofile.timezone))
        else:
            timezone.deactivate()


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        sex = response.get('gender')
        city = response.get('location')['name']
        if sex == 'male':
            sex = '1'
        else:       # female
            sex = '0'
        # profile_timezone = response.get('timezone')

        try:
            user_profile = UserProfile.objects.get(user=user)
            user_profile.sex = sex
            user_profile.city = city
            # profile.timezone = profile_timezone
            user_profile.save()
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user, sex=sex, city=city)
            profile.sex = sex
            profile.city = city
            # profile.timezone = profile_timezone
            profile.save()
