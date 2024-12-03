import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from users.models import ShowProducer 
from hall_manager.models import Category, Slot, Venue, Hall, HallSupportsSlot, HallSupportsCategory

@pytest.fixture
def setup_data(db):
    """
    Fixture to set up in-memory database data for tests.
    """
    # Create user and authenticate client
    user = User.objects.create_user(username="producer", password="password")
    show_producer = ShowProducer.objects.create(user=user)
    client = APIClient()
    client.force_authenticate(user=user)

    # Create necessary data
    category = Category.objects.create(category_name='Music')
    slot = Slot.objects.create(date='2024-10-20', timing='MORNING')
    venue = Venue.objects.create(venue_name="Limerick", location="University of Limerick", phone_number="123456789")
    hall = Hall.objects.create(hall_name="UL", hall_capacity=10, venue=venue)
    HallSupportsSlot.objects.create(hall=hall, slot=slot)
    HallSupportsCategory.objects.create(hall=hall, category=category)

    # Return the created data for use in tests
    return {
        "user": user,
        "show_producer": show_producer,
        "client": client,
        "category": category,
        "slot": slot,
        "venue": venue,
        "hall": hall,
    }
