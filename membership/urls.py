from django.urls import path
from . import views

urlpatterns = [
    path("purchase", views.purchaseMembership),
    path("membership_history", views.get_membership_history),
]
