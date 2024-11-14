from django.db import models
from users.models import ShowProducer
from hall_manager.models import Hall, Slot, Category
from .showstatuses import PendingStatus, ScheduledStatus, CompletedStatus, RejectedStatus, CancelledStatus, ShowStatusEnum

# keep enums in a single file together enums.py
STATUS_CLASSES = {
    ShowStatusEnum.PENDING.name: PendingStatus,
    ShowStatusEnum.SCHEDULED.name: ScheduledStatus,
    ShowStatusEnum.COMPLETED.name: CompletedStatus,
    ShowStatusEnum.REJECTED.name: RejectedStatus,
    ShowStatusEnum.CANCELLED.name: CancelledStatus
}

class Show(models.Model):
    name = models.CharField(max_length=50)
    has_intermission = models.BooleanField()

    STATUS_CHOICES = [(showStatus.name, showStatus.name) for showStatus in ShowStatusEnum]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ShowStatusEnum.PENDING.name)
    
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, related_name="shows")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True, related_name='shows')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="shows")
    show_producer = models.ForeignKey(ShowProducer, on_delete=models.SET_NULL, null=True, related_name='shows')

    def get_status_instance(self):
        status_class = STATUS_CLASSES.get(self.status)
        if status_class:
            return status_class(self)
        raise ValueError(f"Unknown status: {self.status}")

    def approve(self):
        status_instance = self.get_status_instance()
        if(status_instance and not isinstance(status_instance, PendingStatus)):
            raise Exception("Show is not in pending status")
        status_instance.transition_to_scheduled()
    
    def reject(self):
        status_instance = self.get_status_instance()
        if(not isinstance(status_instance, PendingStatus)):
            raise Exception("Show is not in pending status")
        status_instance.transition_to_rejected()
    
    # check if a hall is available to host the show at given slot
    def is_hall_available_at_slot(self, hall, slot):
        has_available_slot = not self.objects.filter(hall=hall, slot=slot).exists()
        return has_available_slot

