import pytest
from rest_framework import status
from rest_framework.test import APIClient
from membership.models import CustomerMembership, MembershipTypeEnum


@pytest.mark.django_db
def test_purchase_membership_success(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    customer = setup_data['customer']

    # Prepare the request data
    data = {
        "membership_type": MembershipTypeEnum.GOLD.name,
        "membership_period": 12
    }

    # Send POST request
    response = client.post('/membership/purchase', data, format="json")
    response_data = response.json()

    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert "Success" in response_data
    assert response_data["Success"] == "Membership purchase is Successful"

    # Verify database changes
    membership = CustomerMembership.objects.filter(customer=customer).first()
    assert membership is not None
    assert membership.membership_type == MembershipTypeEnum.GOLD.name


@pytest.mark.django_db
def test_purchase_membership_invalid_type(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']

    # Prepare the request data
    data = {
        "membership_type": "INVALID_TYPE",
        "membership_period": 12
    }

    # Send POST request
    response = client.post('/membership/purchase', data, format="json")
    response_data = response.json()

    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Invalid membership types are handled by serializer which returns the input given and not an error
    assert 'membership_type' in response_data
    assert response_data['membership_type'] == [
        '"INVALID_TYPE" is not a valid choice.']


@pytest.mark.django_db
def test_customer_purchase_membership_not_authenticated():
    client = APIClient()  # This client is not authenticated

    # Call the customer view tickets API
    response = client.get('/membership/purchase', format="json")

    # Assert the response status is unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert response_data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_membership_history(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    customer_membership = setup_data['customer_membership']

    # Prepare the request
    params = {"page": 1, "limit": 5}

    # Send GET request
    response = client.get('/membership/membership_history', params)
    response_data = response.json()

    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) > 0
    assert response_data[0]["membership_type"] == customer_membership.membership_type
    assert response_data[0]["price"] == customer_membership.price


@pytest.mark.django_db
def test_customer_view_memberships_not_authenticated():
    client = APIClient()  # This client is not authenticated

    # Call the customer view tickets API
    response = client.get('/membership/membership_history', format="json")

    # Assert the response status is unauthorized
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Authentication credentials were not provided."
