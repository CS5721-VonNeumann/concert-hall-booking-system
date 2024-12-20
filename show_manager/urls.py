from django.urls import path
from . import views

urlpatterns = [
    path("raise-request", views.create_update_show_request),
    path("update-scheduled-show", views.update_scheduled_show),
    path("cancel-request", views.cancel_show_request),
    path("cancel-show", views.cancel_show),
    path("list-requests", views.list_show_requests),
    path("scheduled-shows", views.get_scheduled_shows),
    path("list-shows", views.get_all_shows),
]
