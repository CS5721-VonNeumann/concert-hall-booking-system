from threading import local
from django.utils.deprecation import MiddlewareMixin  # Optional for backward compatibility with older Django versions

_thread_locals = local()

def get_current_request():
    # Returns the request object for this thread.
    return getattr(_thread_locals, "request", None)

def get_current_user():
    # Returns the current user, if it exists, otherwise returns None.
    request = get_current_request()
    if request:
        return getattr(request, "user", None)

class CurrentUserMiddleware(MiddlewareMixin):  
    # Simple middleware that adds the request object in thread local storage.

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the current request to thread-local storage
        _thread_locals.request = request
        
        # Get the response after calling the view
        response = self.get_response(request)
        
        # Clean up the thread-local storage
        del _thread_locals.request
        
        return response
