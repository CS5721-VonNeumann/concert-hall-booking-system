from django.urls import path
from . import views

urlpatterns = [
    path("venue/create", views.create_venue, name="create_venue"),
    path("category/create", views.create_category, name="create_category"),
    path("slot/create", views.create_slot, name="create_slot"),
    path("halls/create", views.create_hall, name="create_hall"),
    path("halls/assign_slot", views.assign_slot_to_hall, name="assign_slot_to_hall"),
    path("halls/assign_category", views.assign_category_to_hall, name="assign_category_to_hall"),
    path("halls", views.get_halls, name="get_halls"),
    path("seats/add", views.add_seats_to_hall, name="add_seats_to_hall"),
    path("seats/change_type", views.change_seat_type, name="change_seat_type")
]
