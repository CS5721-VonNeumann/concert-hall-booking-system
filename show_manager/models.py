from django.db import models
from users.models import ShowProducer
from hall_manager.models import Hall
from .showstatuses import PendingStatus, ScheduledStatus, CompletedStatus, RejectedStatus, CancelledStatus, ShowStatusEnum
from enum import Enum

class Slot(models.Model):
    TIMING_CHOICES = [
        ('MORNING', 'MORNING'),
        ('NOON', 'NOON'),
        ('EVENING', 'EVENING'),
        ('NIGHT', 'NIGHT'),
    ]
    date = models.DateField()
    timing = models.CharField(max_length=10, choices=TIMING_CHOICES)

class ShowCategory(Enum):
    LIVE_PERFORMANCE = 'LIVE_PERFORMANCE', 
    MOVIE_SCREENING = 'MOVIE_SCREENING',
    CONFERENCE = 'CONFERENCE'


STATUS_CLASSES = {
    ShowStatusEnum.PENDING.name: PendingStatus,
    ShowStatusEnum.SCHEDULED.name: ScheduledStatus,
    ShowStatusEnum.COMPLETED.name: CompletedStatus,
    ShowStatusEnum.REJECTED.name: RejectedStatus,
    ShowStatusEnum.CANCELLED.name: CancelledStatus
}

class Show(models.Model):
    name = models.CharField(max_length=50)

    CATEGORY_CHOICES = [(category.name, category.name) for category in ShowCategory]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default= ShowCategory.LIVE_PERFORMANCE.name)

    has_intermission = models.BooleanField()
    
    STATUS_CHOICES = [(showStatus.name, showStatus.name) for showStatus in ShowStatusEnum]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ShowStatusEnum.PENDING.name)

    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='shows')
    show_producer = models.ForeignKey(ShowProducer, on_delete=models.SET_NULL, null=True, related_name='shows')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="shows")

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
