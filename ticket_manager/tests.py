import json
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from show_manager.showstatuses import ShowStatusEnum


@pytest.mark.django_db
def test_book_ticket_success(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    show = setup_data['show']
    seats = setup_data['seats']
    # Prepare the request data
    data = {
        "show_id": show.id,
        "seats": [seat.id for seat in seats[1:4]]
    }
    # Send POST request to book tickets
    response = client.post('/ticket_manager/book', data, format="json")
    response_data = response.json()

    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert "ticket_ids" in response_data
    assert len(response_data["ticket_ids"]) > 0
    assert "total_amount" in response_data
    assert response_data["total_amount"] > 0


@pytest.mark.django_db
def test_book_ticket_seat_not_available(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    show = setup_data['show']
    # Simulate unavailable seats by sending invalid seat IDs
    data = {
        "show_id": show.id,
        "seats": [1]  # Invalid seat ID
    }
    # Send POST request to book tickets
    response = client.post('/ticket_manager/book', data, format='json')
    response_data = response.json()
    # Assertions
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data["error"] == "Seat not available."


@pytest.mark.django_db
def test_book_ticket_show_not_available(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    show = setup_data['show']

    # set show status to CANCELLED
    original_status = show.status
    show.status = ShowStatusEnum.CANCELLED.name
    show.save()
    print(show.status)

    # Simulate unavailable seats by sending invalid seat IDs
    data = {
        "show_id": show.id,
        "seats": [1]  # Invalid seat ID
    }
    # Send POST request to book tickets
    response = client.post('/ticket_manager/book', data, format='json')
    response_data = response.json()

    # revert show status
    show.status = original_status
    show.save()

    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response_data
    assert response_data["non_field_errors"][0] == "Ticket cannot be booked for a non-scheduled show."


@pytest.mark.django_db
def test_book_ticket_seat_number_invalid(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    show = setup_data['show']
    # Simulate unavailable seats by sending invalid seat IDs
    data = {
        "show_id": show.id,
        "seats": [999]  # Invalid seat ID
    }
    # Send POST request to book tickets
    response = client.post('/ticket_manager/book', data, format='json')
    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_book_tickets_not_authenticated():
    client = APIClient()  # This client is not authenticated

    # Call the customer view tickets API
    response = client.get('/ticket_manager/book', format="json")

    # Assert the response status is unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert response_data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_ticket_history_success(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    # Prepare the request data
    response = client.get('/ticket_manager/view_history', format="json")
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)  # Expecting a list of tickets


@pytest.mark.django_db
def test_get_ticket_history_no_tickets(setup_data):
    # Setup from fixture
    client = setup_data['client_customer']
    customer = setup_data['customer']
    # Clear all tickets related to customer for this test
    customer.tickets.all().delete()
    # Prepare the request data
    response = client.get('/ticket_manager/view_history', format="json")
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []  # Expecting an empty list of tickets


@pytest.mark.django_db
def test_view_ticket_history_not_authenticated():
    client = APIClient()  # This client is not authenticated

    # Call the customer view tickets API
    response = client.get('/ticket_manager/view_history', format="json")

    # Assert the response status is unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert response_data["detail"] == "Authentication credentials were not provided."

@pytest.mark.django_db
def test_cancel_ticket(setup_data):
    client = setup_data["client_customer"]
    ticket = setup_data["ticket"]

    # Prepare request data
    request_data = {
        "ticket_ids": [ticket.id]
    }

    # Make the POST request to cancel the ticket
    response = client.post('/ticket_manager/cancel_ticket',
                           request_data, format="json")

    response_data = json.loads(response.content.decode())
    # Check the response status
    assert response.status_code == 200

    # Validate the response data
    assert response_data["status"] == "success"
    assert "tickets" in response_data
    assert len(response_data["tickets"]) == 1
    assert response_data["tickets"][0] == ticket.id


@pytest.mark.django_db
def test_cancel_ticket_not_authenticated(setup_data):
    client = APIClient()  # This client is not authenticated
    ticket = setup_data["ticket"]

    cancel_data = {
        "ticket_ids": [ticket.id],
    }

    response = client.post('/ticket_manager/cancel_ticket',
                           cancel_data, format="json")

    # Assert the response status is unauthorized
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_cancel_ticket_invalid_ticket(setup_data):
    client = setup_data["client_customer"]

    # Try canceling a ticket with an invalid ID
    cancel_data = {
        "ticket_ids": [9999],  # Assuming 9999 does not exist
    }

    response = client.post('/ticket_manager/cancel_ticket',
                           cancel_data, format="json")

    # Assert the response status is error
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["status"] == "error"
    assert response_data["errors"]["ticket_ids"][0] == "Invalid ticket ID 9999 or the ticket does not belong to you."


@pytest.mark.django_db
def test_customer_view_tickets(setup_data):
    client = setup_data["client_customer"]
    ticket = setup_data["ticket"]

    # Call the customer view tickets API
    response = client.get('/ticket_manager/booked-tickets', format="json")

    # Assert the response status is success
    assert response.status_code == 200
    response_data = response.json()

    # Check if the ticket is in the response data
    assert len(response_data) == 1
    ticket_data = response_data[0]

    # Check that the ticket data matches the expected values
    assert ticket_data["show"] == ticket.show.name
    assert ticket_data["venue"] == ticket.seat.hall.hall_name
    assert ticket_data["date"] == ticket.getShowDate()
    assert ticket_data["time"] == ticket.getShowTimimg()


@pytest.mark.django_db
def test_customer_view_tickets_not_authenticated():
    client = APIClient()  # This client is not authenticated

    # Call the customer view tickets API
    response = client.get('/ticket_manager/booked-tickets', format="json")

    # Assert the response status is unauthorized
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Authentication credentials were not provided."

@pytest.mark.django_db
def test_admin_view_ticket_sales(setup_data):
    client_admin = setup_data["client_admin"]
    show_obj = setup_data["show"]

    # Call the view ticket sales API for admin
    response = client_admin.post(
        "/ticket_manager/view-sales", 
        {"show_name": show_obj.name},
        format="json"
    )
    # Assert response
    assert response.status_code == 200

@pytest.mark.django_db
def test_show_producer_view_ticket_sales_with_no_slotid(setup_data):
    client_show_producer = setup_data["client_showproducer"]
    show_obj = setup_data["show"]

    # Call the view ticket sales API for show producer
    response = client_show_producer.post(
        "/ticket_manager/view-sales", 
        {"show_name": show_obj.name},
        format="json"
    )
    # Assert response
    assert response.status_code == 400

@pytest.mark.django_db
def test_show_producer_view_ticket_sales(setup_data):
    client_show_producer = setup_data["client_showproducer"]
    show_obj = setup_data["show"]
    
    # Call the view ticket sales API for show producer
    response = client_show_producer.post(
        "/ticket_manager/view-sales", 
        {"show_name": show_obj.name,"slot_id":show_obj.slot.id},
        format="json"
    )
    # Assert response
    assert response.status_code == 200

@pytest.mark.django_db
def test_customer_view_ticket_sales_unauthorized(setup_data):
    client_customer = setup_data["client_customer"]
    show_obj = setup_data["show"]

    # Attempt to access the sales data as a customer
    response = client_customer.post(
        "/ticket_manager/view-sales", 
        {"show_name": show_obj.name},
        format="json"
    )

    # Assert unauthorized access error
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized access"}

@pytest.mark.django_db
def test_invalid_show_name_admin_view_sales(setup_data):
    client_admin = setup_data["client_admin"]

    # Attempt to fetch ticket sales for a non-existent show
    response = client_admin.post(
        "/ticket_manager/view-sales", 
        {"show_name": "NonExistentShow"},
        format="json"
    )

    # Assert error due to invalid show name
    assert response.status_code == 400
