import pytest
from django.contrib.auth.models import User
from show_manager.models import Show, ShowStatusEnum
from users.models import ShowProducer
from .engine_cor import ApprovalEngine
from hall_manager.models import Category, Slot, Hall, HallSupportsCategory, HallSupportsSlot, Venue
from notifications.models import ShowProducerNotifications

@pytest.mark.django_db
def test_worker_rejects_invalid_request(setup_data, mocker):
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    category2 = Category.objects.create(category_name="Drama")
    slot2 = Slot.objects.create(date="2024-12-31", timing="MORNING")


    show = Show.objects.create(
        name="Invalid Show",
        status=ShowStatusEnum.PENDING.name,
        show_producer=show_producer,
        category=category2,
        slot=slot2,
        hall=hall,
        has_intermission=True
    )

    mock_notify = mocker.patch("show_manager.models.Show.notify")
    
    ApprovalEngine(show=show).handle_show_request()
    show.refresh_from_db()
    assert show.status == ShowStatusEnum.REJECTED.name
    mock_notify.assert_called_with(interest=0, message="Validation failed: The hall does not support this show category.")

    show.status = ShowStatusEnum.PENDING.name
    show.category = category
    show.save()

    ApprovalEngine(show=show).handle_show_request()
    show.refresh_from_db()
    assert show.status == ShowStatusEnum.REJECTED.name
    mock_notify.assert_called_with(interest=0, message="Validation failed: The hall does not support this show slot.")

    show2 = Show.objects.create(
        name="Overlapping Show",
        status=ShowStatusEnum.SCHEDULED.name,
        show_producer=show_producer,
        category=category,
        slot=slot,
        hall=hall,
        has_intermission=True
    )

    show.status = ShowStatusEnum.PENDING.name
    show.slot = slot
    show.save()

    ApprovalEngine(show=show).handle_show_request()
    show.refresh_from_db()
    assert show.status == ShowStatusEnum.REJECTED.name
    mock_notify.assert_called_with(interest=0, message="Another show is already scheduled in the same hall and slot.")



@pytest.mark.django_db
def test_worker_approves_valid_request_and_notify(setup_data, mocker):
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

    mock_notify = mocker.patch("show_manager.models.Show.notify")

    ApprovalEngine(show=show).handle_show_request()
    show.refresh_from_db()
    assert show.status == ShowStatusEnum.SCHEDULED.name
    mock_notify.assert_called_with(interest=0)
