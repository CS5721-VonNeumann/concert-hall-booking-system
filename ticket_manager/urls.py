from django.urls import path
from . import views

urlpatterns = [
    path("book", views.bookTickets),
    path("view_history", views.get_ticket_history),
    path('booked-tickets',views.customer_view_tickets),

]
