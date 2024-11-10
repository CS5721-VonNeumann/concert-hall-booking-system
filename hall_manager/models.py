from django.db import models

class Hall(models.Model):
    hall_name = models.CharField(max_length=30)
    hall_capacity = models.IntegerField()