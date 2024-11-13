from django.db import models
from shared.interfaces import Observer
from notifications.models import ShowProducerNotifications

class ShowProducer(models.Model, Observer):
    email = models.EmailField(unique=True)

    def update(self, message):
        """
        This method is called by the Subject (Show) when its status changes.
        """
        ShowProducerNotifications.objects.create(
            show_producer=self,
            message=message,
            isRead=False
        )



class Customer(models.Model):
    loyaltyPoints = models.IntegerField()
