from django.db import models
from users.models import ShowProducer
from hall_manager.models import Hall, Slot, Category
from .showstatuses import PendingStatus, ScheduledStatus, CompletedStatus, RejectedStatus, CancelledStatus, ShowStatusEnum
from shared.interfaces import Subject

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

    def attach(self, observer, interest):
        if(interest == 0):
            # observer is interested in show approval / rejection
            # show producer is stored inside show table
            self.show_producer = observer
            self.save()
        # TODO 
        # when customer purchases ticket, he will attach with interest = 1 to know show cancellations
        pass

    def notify(self, interest, message = ""):
        """
        Notify the registered observer (show producer) about the status change.
        """
        if(interest == 0):
            self.show_producer.update(f"Show '{self.name}' status changed to {self.status}. {message}")
        # TODO 
        # on cancellation, notify customers who purchased tickets for this show
        pass

    def get_status_instance(self):
        status_class = STATUS_CLASSES.get(self.status)
        if status_class:
            return status_class(self)
        raise ValueError(f"Unknown status: {self.status}")

    def schedule(self):
        status_instance = self.get_status_instance()
        if(status_instance and not isinstance(status_instance, PendingStatus)):
            raise Exception("Show is not in pending status")
        status_instance.transition_to_scheduled()
        self.notify(interest=0)
    
    def reject(self, message):
        status_instance = self.get_status_instance()
        if(not isinstance(status_instance, PendingStatus)):
            raise Exception("Show is not in pending status")
        status_instance.transition_to_rejected()
        self.notify(interest=0, message=message)

    @staticmethod
    def is_overlapping_show_exists(hall, slot):
        overlapping_shows = Show.objects.filter(
            hall=hall, 
            slot=slot,
            status=ShowStatusEnum.SCHEDULED.name
        ).exists()
        return overlapping_shows

    
