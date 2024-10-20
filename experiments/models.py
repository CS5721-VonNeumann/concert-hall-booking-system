from django.db import models

# Create your models here.
class Shows(models.Model):
    Name = models.CharField(max_length=255)
    Category = models.CharField(max_length=20)

class Seats(models.Model):
    SeatNumber = models.IntegerField()
    SeatType = models.CharField(max_length=10)