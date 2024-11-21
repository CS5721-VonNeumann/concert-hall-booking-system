from django.db import models
from users.models import Customer
from hall_manager.models import Hall,Seat
from show_manager.models import Show

# Create your models here.
class Ticket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="tickets")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="tickets")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="tickets")
    
    isCancelled = models.BooleanField(default=False)
    
