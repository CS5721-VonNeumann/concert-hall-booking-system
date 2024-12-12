import pytest
from django.urls import reverse

from show_manager.models import Show, ShowStatusEnum
from notifications.models import ShowProducerNotifications, CustomerNotifications
from approval_engine.engine_cor import ApprovalEngine

@pytest.mark.django_db
def test_notification_for_rejected_show(setup_data):
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    show = Show.objects.create(
        name="Invalid Show",
        status=ShowStatusEnum.PENDING.name,
        show_producer=show_producer,
        category=category,
        slot=slot,
        hall=hall,
        has_intermission=True
    )

    show2 = Show.objects.create(
        name="Overlapping Show",
        status=ShowStatusEnum.SCHEDULED.name,
        show_producer=show_producer,
        category=category,
        slot=slot,
        hall=hall,
        has_intermission=True
    )

    ApprovalEngine(show=show).handle_show_request()
    show.refresh_from_db()
    assert show.status == ShowStatusEnum.REJECTED.name

    notification = ShowProducerNotifications.objects.filter().last()
    assert notification.message == "Show 'Invalid Show' status changed to REJECTED. Another show is already scheduled in the same hall and slot."


@pytest.mark.django_db
def test_get_show_producer_notifications(setup_data):
    client_showproducer = setup_data["client_showproducer"]
    show_producer = setup_data["show_producer"]

    # Create unread notifications for the show producer
    ShowProducerNotifications.objects.create(show_producer=show_producer, isRead=False, message="Notification 1")
    ShowProducerNotifications.objects.create(show_producer=show_producer, isRead=False, message="Notification 2")

    # Fetch unread notifications
    url = reverse("get_show_producer_notifications")
    response = client_showproducer.get(url)

    assert response.status_code == 200
    notifications = response.json()["notifications_response"]
    assert len(notifications) == 2
    assert notifications[0]["message"] == "Notification 1"
    assert notifications[1]["message"] == "Notification 2"


@pytest.mark.django_db
def test_mark_show_producer_notifications_as_read(setup_data):
    client_producer = setup_data["client_showproducer"]
    show_producer = setup_data["show_producer"]

    # Create an unread notification
    notification = ShowProducerNotifications.objects.create(show_producer=show_producer, isRead=False, message="Notification to mark")

    # Mark the notification as read
    url = reverse("mark_show_producer_notifications_as_read", args=[notification.id])
    response = client_producer.patch(url)

    assert response.status_code == 200
    assert response.json()["message"] == "Notification marked as read successfully"

    # Verify that the notification was updated in the database
    notification.refresh_from_db()
    assert notification.isRead is True

@pytest.mark.django_db
def test_get_customer_notifications(setup_data):
    client_customer = setup_data["client_customer"]
    customer = setup_data["customer"]

    # Create unread notifications for the customer
    CustomerNotifications.objects.create(customer=customer, isRead=False, message="Notification 1")
    CustomerNotifications.objects.create(customer=customer, isRead=False, message="Notification 2")

    # Fetch unread notifications
    response = client_customer.get(reverse("get_customer_notifications"))

    assert response.status_code == 200
    notifications = response.json()["notifications_response"]
    assert len(notifications) == 2
    assert notifications[0]["message"] == "Notification 1"
    assert notifications[1]["message"] == "Notification 2"


@pytest.mark.django_db
def test_get_customer_notifications_no_unread(setup_data):
    client_customer = setup_data["client_customer"]
    customer = setup_data["customer"]

    # Ensure no unread notifications exist
    CustomerNotifications.objects.filter(customer=customer).update(isRead=True)

    # Fetch unread notifications
    response = client_customer.get(reverse("get_customer_notifications"))

    assert response.status_code == 200
    notifications = response.json()["notifications_response"]
    assert len(notifications) == 0


@pytest.mark.django_db
def test_mark_customer_notifications_as_read_valid(setup_data):
    client_customer = setup_data["client_customer"]
    customer = setup_data["customer"]

    # Create an unread notification
    notification = CustomerNotifications.objects.create(customer=customer, isRead=False, message="Notification 1")

    # Mark the notification as read
    url = reverse("mark_customer_notifications_as_read", args=[notification.id])
    response = client_customer.patch(url)

    assert response.status_code == 200
    assert response.json()["message"] == "Notification marked as read successfully"

    # Ensure the notification is marked as read
    notification.refresh_from_db()
    assert notification.isRead is True


@pytest.mark.django_db
def test_mark_customer_notifications_as_read_invalid_id(setup_data):
    client_customer = setup_data["client_customer"]

    # Attempt to mark a non-existent notification as read
    url = reverse("mark_customer_notifications_as_read", args=[999])
    response = client_customer.patch(url)

    assert response.status_code == 404
    assert response.json()["error"] == "Invalid notification ID"