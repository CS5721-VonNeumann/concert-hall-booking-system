from django.db import models

class ShowProducer(models.Model):
    email = models.EmailField(unique=True)