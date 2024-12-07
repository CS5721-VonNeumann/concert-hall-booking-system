from django.urls import path
from . import views

urlpatterns = [
    path("purchase", views.purchase_membership),
    path("membership_history", views.get_membership_history),
]
