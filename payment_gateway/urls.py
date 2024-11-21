from django.urls import path
from . import views

urlpatterns = [
    path("history", views.get_transaction_history),
]
