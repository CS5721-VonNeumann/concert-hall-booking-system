from django.urls import path
from . import views

urlpatterns = [
    path("show-producer", views.get_show_producer_notifications, name="get_show_producer_notifications"),
    path("mark-as-read-show-producer/<int:notification_id>", views.mark_show_producer_notifications_as_read, name="mark_show_producer_notifications_as_read"),
    path("customer", views.get_customer_notifications, name="get_customer_notifications"),
    path("mark-as-read-customer/<int:notification_id>", views.mark_customer_notifications_as_read, name="mark_customer_notifications_as_read")
]
