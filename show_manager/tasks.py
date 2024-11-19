from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from show_manager.models import Show, ShowStatusEnum

@shared_task
def mark_shows_as_completed():
    print("Running mark_shows_as_completed cron job")
    yesterday = (now() - timedelta(1)).strftime('%Y-%m-%d')
    shows_to_complete = Show.objects.filter(
        slot__date__lte=yesterday,
        status = ShowStatusEnum.SCHEDULED.name
    )

    for show in shows_to_complete:
        show.complete()
        print(f"Show '{show.name}' marked as completed.")