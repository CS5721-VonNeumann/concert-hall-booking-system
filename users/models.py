from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    phone = models.CharField(max_length=15, default="")
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Customer)"

class ShowProducer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    phone = models.CharField(max_length=15, default="")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Show Producer)"
