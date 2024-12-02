from django.urls import path
from . import views

urlpatterns = [
    path("raise-request", views.create_update_show_request),
    path("update-scheduled-show", views.update_scheduled_show),
    path("cancel-request", views.cancel_show_request),
    path("list-requests", views.list_show_requests),
]
