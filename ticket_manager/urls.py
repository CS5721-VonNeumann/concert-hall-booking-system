from django.urls import path
from . import views

urlpatterns = [
    path("book", views.book_tickets),
    path("view_history", views.get_ticket_history),
    path('booked-tickets',views.customer_view_tickets),
    path("cancel_ticket", views.cancel_ticket),  
    path("view-sales",views.view_ticket_sales),
]
