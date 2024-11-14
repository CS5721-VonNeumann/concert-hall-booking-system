from django.urls import path
from . import views

urlpatterns = [
    path("venue/create", views.create_venue),
    path("category/create", views.create_category),
    path("slot/create", views.create_slot),
    path("halls/create", views.create_hall),
    path("halls/assign_slot", views.assign_slot_to_hall),
    path("halls/assign_category", views.assign_category_to_hall),
    path("halls", views.get_halls),
]
