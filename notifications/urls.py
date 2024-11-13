from django.urls import path
from . import views

urlpatterns = [
    # TODO update this route based on login middleware
    path("show-producer", views.get_show_producer_notifications),
    path("mark-as-read-show-producer/<int:notification_id>", views.mark_show_producer_notifications_as_read)
]
