from django.urls import path
from . import views

urlpatterns = [
    path("raise-request", views.create_show_request),
]
