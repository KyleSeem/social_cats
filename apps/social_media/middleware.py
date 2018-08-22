from django.utils.deprecation import MiddlewareMixin

from threading import local

_user = local()

class GetCurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _user.id = request.user.id

def get_current_user():
    return _user.id
