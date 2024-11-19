from celery import shared_task
from django.utils.timezone import now
from show_manager.models import Show, ShowStatusEnum

@shared_task
def mark_shows_as_completed():
    current_time = now().date()  # Current date
    shows_to_complete = Show.objects.filter(
        slot__date__lt=current_time,
        status = ShowStatusEnum.SCHEDULED.name
    )

    for show in shows_to_complete:
        show.complete()
        print(f"Show '{show.name}' marked as completed.")