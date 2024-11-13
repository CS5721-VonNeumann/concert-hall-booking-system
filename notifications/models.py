from django.db import models
from users.models import ShowProducer
from hall_manager.models import Hall, Slot, Category

class ShowProducerNotifications(models.Model):
    show_producer = models.ForeignKey(ShowProducer, on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=100)
    isRead = models.BooleanField(default=False)