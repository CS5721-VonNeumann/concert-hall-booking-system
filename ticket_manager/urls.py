from django.urls import path
from . import views

urlpatterns = [
    path("book", views.bookTickets),
    path("view_history", views.get_ticket_history),
    path("view-sales",views.view_ticket_sales),
]
