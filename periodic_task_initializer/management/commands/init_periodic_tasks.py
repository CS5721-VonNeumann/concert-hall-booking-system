from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from django.utils import timezone

class Command(BaseCommand):
    help = "Initialize periodic tasks"

    def handle(self, *args, **kwargs):
        # Create or fetch an interval schedule
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,  # Every 1 day
            period=IntervalSchedule.DAYS,
        )

        # Define or update a periodic task
        task_name = "mark_shows_as_completed"
        PeriodicTask.objects.get_or_create(
            name=task_name,
            defaults={
                "interval": schedule,
                "task": "show_manager.tasks.mark_shows_as_completed",  # Full path to the task
                "start_time": timezone.now(),
                "args": json.dumps([]),
                "kwargs": json.dumps({}),
            },
        )

        self.stdout.write(self.style.SUCCESS(f"Periodic task '{task_name}' initialized."))