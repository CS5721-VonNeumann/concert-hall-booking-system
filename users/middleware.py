from threading import local
from django.utils.deprecation import MiddlewareMixin  
from django.contrib.auth.models import AnonymousUser

_thread_locals = local()

def get_current_user():
    # Returns the current user, if it exists, otherwise returns None.
    request = getattr(_thread_locals, "request", None)
    if request:
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            return user
    return None  

class CurrentUserMiddleware(MiddlewareMixin):  
    # Simple middleware that adds the request object in thread local storage.
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)        
        del _thread_locals.request
        return response
