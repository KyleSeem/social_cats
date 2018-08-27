from django.utils.deprecation import MiddlewareMixin

from threading import local
import pytz
from django.utils import timezone

_user = local()

class GetCurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _user.id = request.user.id

def get_current_user():
    return _user.id


class TimeZoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
