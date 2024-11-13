from django.db import models

class ShowProducerNotifications(models.Model):
    show_producer = models.ForeignKey('users.ShowProducer', on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=100)
    isRead = models.BooleanField(default=False)