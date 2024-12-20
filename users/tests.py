import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from users.models import ShowProducer, Customer

@pytest.mark.django_db
def test_register_showproducer():
    client = APIClient()
    data = {
        "email": "showproducer@example.com",
        "phone": "1234567890",
        "password": "strongpassword",
        "first_name": "Jacob",
        "last_name": "March",
        "organisation": "ExampleOrg"
    }

    response = client.post("/users/showproducer/register", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "token" in response.data
    assert ShowProducer.objects.filter(phone=data["phone"]).exists()

    # Verify the linked user
    user = User.objects.get(email=data["email"])
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]

@pytest.mark.django_db
def test_showproducer_login():
    # Set up initial user and show producer
    client = APIClient()
    email = "showproducer@example.com"
    password = "strongpassword"
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name="Jacob",
        last_name="March"
    )
    ShowProducer.objects.create(user=user, phone="1234567890", organisation="ExampleOrg")

    # Attempt login
    response = client.post("/users/login", {"email": email, "password": password})

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["email"] == email
    assert response.data["profile_type"] == "ShowProducer"

@pytest.mark.django_db
def test_register_customer_success():
    client = APIClient()
    data = {
        "email": "testcustomer@example.com",
        "phone": "+1234567890",
        "password": "strongpassword",
        "first_name": "John",
        "last_name": "Doe",
        "organisation": "ExampleOrg"
    }

    response = client.post("/users/customer/register", data)
    
    # Assert that the response returns a 201 status code
    assert response.status_code == status.HTTP_201_CREATED

    # Assert the response contains a token
    assert "token" in response.data

@pytest.mark.django_db
def test_register_customer_invalid_data():
    client = APIClient()
    data = {
        # Missing required fields like email and password
        "phone": "+1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "organisation": "ExampleOrg"
    }

    response = client.post("/users/customer/register", data)
    
    # Assert that the response returns a 400 status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Assert the response contains error messages
    assert "email" in response.data  # Email is missing
    assert "password" in response.data  # Password is missing

@pytest.mark.django_db
def test_customer_login():
    # Create a test user and customer
    client = APIClient()
    email = "customer@example.com"
    password = "securepassword"
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name="Lana",
        last_name="Tims"
    )
    Customer.objects.create(user=user, phone="1234567890")

    # Attempt to log in
    response = client.post("/users/login", {"email": email, "password": password})

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["email"] == email
    assert response.data["profile_type"] == "Customer"

@pytest.mark.django_db
def test_admin_login():
    client = APIClient()

    # Create a superuser (admin)
    email = "admin@example.com"
    password = "secureadminpassword"
    admin_user = User.objects.create_superuser(
        username=email,
        email=email,
        password=password
    )

    # Attempt to log in as admin
    response = client.post("/users/admin/login", {"email": email, "password": password})

    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["message"] == "Admin logged in"

    # Check token validity
    token = response.data["token"]
    assert admin_user.auth_token.key == token
