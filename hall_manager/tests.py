import pytest
from rest_framework import status
from django.urls import reverse
from hall_manager.models import Hall, Slot, Category, Seat, HallSupportsCategory, HallSupportsSlot

@pytest.mark.django_db
class TestHallManagerViews:

    def test_create_hall(self, setup_data):
        client = setup_data["client_admin"]
        url = reverse("create_hall")
        data = {"hall_name": "New Hall", "hall_capacity": 100, "venue": setup_data["venue"].id}
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['message'] == "Hall created successfully"
        assert Hall.objects.filter(hall_name="New Hall").exists()

    def test_create_slot(self, setup_data):
        client = setup_data["client_admin"]
        url = reverse("create_slot")
        data = {"date": "2025-11-25", "timing": "EVENING"}
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['message'] == "Slot created successfully"
        assert Slot.objects.filter(timing="EVENING").exists()

    def test_create_category(self, setup_data):
        client = setup_data["client_admin"]
        url = reverse("create_category")
        data = {"category_name": "Conference"}
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['message'] == "Category created successfully"
        assert Category.objects.filter(category_name="Conference").exists()

    def test_assign_slot_to_hall(self, setup_data):
        client = setup_data["client_admin"]
        url = reverse("assign_slot_to_hall")
        data = {"hall_id": setup_data["hall"].id, "slot_id": setup_data["slot"].id}
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['message'] == "Slot assigned to hall successfully"
        assert HallSupportsSlot.objects.filter(hall=setup_data["hall"], slot=setup_data["slot"]).exists()

    def test_assign_category_to_hall(self, setup_data):
        client = setup_data["client_admin"]
        url = reverse("assign_category_to_hall")
        data = {"hall_id": setup_data["hall"].id, "category_id": setup_data["category"].id}
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['message'] == "Category assigned to hall successfully"
        assert HallSupportsCategory.objects.filter(hall=setup_data["hall"], category=setup_data["category"]).exists()

    def test_get_halls(self, setup_data):
        client = setup_data["client_admin"]
        url = reverse("get_halls") + "?category_id=" + str(setup_data["category"].id) + "&slot_id=" + str(setup_data["slot"].id)
        
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'halls_response' in response.json()


    def test_permission_denied_for_non_superuser(self, setup_data):
        client = setup_data["client_showproducer"]
        url = reverse("add_seats_to_hall")
        data = {"hall_id": setup_data["hall"].id, "seat_numbers": [5, 6, 7, 8]}
        
        response = client.put(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Permission denied" in response.json()['error']

    def test_permission_denied_for_non_authenticated_user(self, setup_data):
        client = setup_data["client"]
        url = reverse("create_hall")
        data = {"hall_name": "Unauthorized Hall", "hall_capacity": 100, "venue": setup_data["venue"].id}
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
