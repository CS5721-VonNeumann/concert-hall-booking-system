import pytest
from django.contrib.auth.models import User
from show_manager.models import Show, ShowStatusEnum
from users.models import ShowProducer
from approval_engine.engine_cor import ApprovalEngine
from hall_manager.models import Category, Slot, Hall, HallSupportsCategory, HallSupportsSlot, Venue
from notifications.models import ShowProducerNotifications

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
def test_notification_for_scheduled_show(setup_data, mocker):
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    show = Show.objects.create(
        name="Valid Show",
        status=ShowStatusEnum.PENDING.name,
        show_producer=show_producer,
        category=category,
        slot=slot,
        hall=hall,
        has_intermission=True
    )

    ApprovalEngine(show=show).handle_show_request()
    show.refresh_from_db()
    assert show.status == ShowStatusEnum.SCHEDULED.name
    notification = ShowProducerNotifications.objects.filter().last()
    print(notification.message)
    assert notification.message == "Show 'Valid Show' status changed to SCHEDULED. "


    