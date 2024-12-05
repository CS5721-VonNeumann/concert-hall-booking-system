from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from users.models import Customer
from hall_manager.models import Seat
from show_manager.models import Show

# Create your models here.
class Ticket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="tickets")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="tickets")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="tickets")
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=6,
        null=False,
        validators=[MinValueValidator(Decimal('0.00'))]
        )
    
    isCancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def cancel(self):
        self.isCancelled = True
        self.save()

    def getShowTimimg(self):
        return (self.show.slot.timing)

    def getShowDate(self):
        return self.show.slot.date
