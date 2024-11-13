from celery import shared_task
from show_manager.models import Show
from .engine import ApprovalEngine

@shared_task
def handle_show_request(show_id):
    try:
        show = Show.objects.get(id=show_id)
        approval_engine = ApprovalEngine(show)
        approval_engine.handle_show_request()
    except Show.DoesNotExist:
        print(f"Show with ID {show_id} does not exist.")