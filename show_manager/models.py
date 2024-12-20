from django.db import models
from users.models import ShowProducer
from hall_manager.models import Hall, Slot, Category
from .showstatuses import ShowStatus, PendingStatus, ScheduledStatus, CompletedStatus, RejectedStatus, CancelledStatus, ShowStatusEnum
from shared.interfaces import Subject
from .constants import (
    INVALID_SCHEDULED_STATUS_ERROR,
    INVALID_PENDING_STATUS_ERROR,
)

# keep enums in a single file together enums.py
STATUS_CLASSES = {
    ShowStatusEnum.PENDING.name: PendingStatus,
    ShowStatusEnum.SCHEDULED.name: ScheduledStatus,
    ShowStatusEnum.COMPLETED.name: CompletedStatus,
    ShowStatusEnum.REJECTED.name: RejectedStatus,
    ShowStatusEnum.CANCELLED.name: CancelledStatus
}

class Show(models.Model, Subject):
    name = models.CharField(max_length=50)
    has_intermission = models.BooleanField()

    STATUS_CHOICES = [(showStatus.name, showStatus.name) for showStatus in ShowStatusEnum]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ShowStatusEnum.PENDING.name)
    
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, related_name="shows")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True, related_name='shows')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="shows")
    show_producer = models.ForeignKey(ShowProducer, on_delete=models.SET_NULL, null=True, related_name='shows')

    def attach(self, observer):
        # observer is interested in show approval / rejection
        # show producer is stored inside show table
        self.show_producer = observer
        self.save()

    def notify(self, message=""):
        # notify the registered observer (show producer) about the status change.
        self.show_producer.update(f"Show '{self.name}' status changed to {self.status}. {message}")

    def get_status_instance(self):
        status_class = STATUS_CLASSES.get(self.status)
        if status_class:
            return status_class(self)
        raise ValueError(f"Unknown status: {self.status}")

    def schedule(self):
        status_instance: ShowStatus = self.get_status_instance()
        if(status_instance and not isinstance(status_instance, PendingStatus)):
            raise ValueError(INVALID_PENDING_STATUS_ERROR)
        status_instance.transition_to_scheduled()
        self.notify()

    def reject(self, message):
        status_instance: ShowStatus = self.get_status_instance()
        if(not isinstance(status_instance, PendingStatus)):
            raise ValueError(INVALID_PENDING_STATUS_ERROR)
        status_instance.transition_to_rejected()
        self.notify(message=message)
    
    def cancel(self, message=""):
        status_instance: ShowStatus = self.get_status_instance()
        # producer is cancelling a pending show, no need for notifications
        if(status_instance and isinstance(status_instance, PendingStatus)):
            status_instance.transition_to_cancelled()

        if(status_instance and isinstance(status_instance, ScheduledStatus)):
            status_instance.transition_to_cancelled()
            self.notify(message=message)

    def complete(self):
        status_instance: ShowStatus = self.get_status_instance()
        if(not isinstance(status_instance, ScheduledStatus)):
            raise ValueError(INVALID_SCHEDULED_STATUS_ERROR)
        status_instance.transition_to_completed()

    @staticmethod
    def is_overlapping_show_exists(hall, slot):
        overlapping_shows = Show.objects.filter(
            hall=hall, 
            slot=slot,
            status=ShowStatusEnum.SCHEDULED.name
        ).exists()
        return overlapping_shows
