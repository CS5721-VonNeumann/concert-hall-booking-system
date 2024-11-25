from celery import shared_task
from show_manager.models import Show
from .engine_cor import ApprovalEngine
from config.celery import BaseTaskWithRetry

@shared_task(base=BaseTaskWithRetry, acks_late=True)
def handle_show_request(show_id):
    try:
        show = Show.objects.get(id=show_id)
    except Show.DoesNotExist:
        print(f"Show with ID {show_id} does not exist.")
        return

    approval_engine = ApprovalEngine(show)
    approval_engine.handle_show_request()