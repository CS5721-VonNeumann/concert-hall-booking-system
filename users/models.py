from django.contrib.auth.models import User
from django.db import models
from shared.interfaces import Observer, MultiBaseMeta
from notifications.models import ShowProducerNotifications

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    phone = models.CharField(max_length=15, default="")
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Customer)"

class ShowProducer(models.Model, Observer, metaclass=MultiBaseMeta):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    phone = models.CharField(max_length=15, default="")
    organisation = models.CharField(max_length=30, default="")
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Show Producer)"
    
    def update(self, message):
        """
        This method is called by the Subject (Show) when its status changes.
        """
        ShowProducerNotifications.objects.create(
            show_producer=self,
            message=message,
            isRead=False
        )
