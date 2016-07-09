import pytz
from django.utils import timezone


class TimezoneMiddleware(object):

    def process_request(self, request):
        # pass
        if request.user.is_authenticated():
           timezone.activate(pytz.timezone(request.user.userprofile.timezone))
        else:
            timezone.deactivate()