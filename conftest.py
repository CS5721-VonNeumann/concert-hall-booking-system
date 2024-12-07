from importlib import import_module
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from users.models import Customer, ShowProducer 
from hall_manager.models import Category, Slot, Venue, Hall, HallSupportsSlot, HallSupportsCategory
from show_manager.models import Show, ShowStatusEnum
from ticket_manager.models import Ticket

@pytest.fixture
def setup_data(db):
    """
    Fixture to set up in-memory database data for tests.
    """
    # Create user and authenticate client
    user = User.objects.create_user(username="producer", password="password")
    show_producer = ShowProducer.objects.create(user=user)
    user_new = User.objects.create_user(username="customer", password="password")
    customer = Customer.objects.create(user=user_new)
    client = APIClient()
    client.force_authenticate(user=user)
    client_customer = APIClient()
    client_customer.force_authenticate(user=user_new)
    admin_user = User.objects.create_superuser(
        username='admin', password='adminpassword', email='admin@example.com'
    )
    # Authenticate for testing
    client_admin = APIClient()
    client_admin.force_authenticate(user=admin_user)
    # Create necessary data
    category = Category.objects.create(category_name='Music')
    slot = Slot.objects.create(date='2025-10-20', timing='MORNING')
    venue = Venue.objects.create(venue_name="Limerick", location="University of Limerick", phone_number="123456789")
    hall = Hall.objects.create(hall_name="UL", hall_capacity=10, venue=venue)
    HallSupportsSlot.objects.create(hall=hall, slot=slot)
    HallSupportsCategory.objects.create(hall=hall, category=category)

    # Create a ticket for cancellation
    show_obj = Show.objects.create(name="Test Show", 
                                   category=category, 
                                   hall=hall, 
                                   slot=slot, 
                                   status=ShowStatusEnum.PENDING,
                                   has_intermission=True
                                   )
    ticket = Ticket.objects.create(customer=customer, show=show_obj, seat=hall.seats.first(), price=10.00)

    # Return the created data for use in tests
    return {
        "user": user,
        "show_producer": show_producer,
        "client": client,
        "category": category,
        "slot": slot,
        "venue": venue,
        "hall": hall,
        "customer": customer,
        "ticket": ticket,
        "client_customer": client_customer,
        "admin": admin_user,
        "client_admin":client_admin,
        "show": show_obj
    }
