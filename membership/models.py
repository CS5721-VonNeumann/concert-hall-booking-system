from django.db import models
from users.models import Customer

class CustomerMembership(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customermemberships")
    membership_type = models.CharField(max_length=10)
    price = models.FloatField(default=0)
    expiry = models.DateTimeField()
