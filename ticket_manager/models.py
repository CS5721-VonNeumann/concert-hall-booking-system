from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

from shared.interfaces import Subject
from users.models import Customer
from hall_manager.models import Seat
from show_manager.models import Show
from show_manager.showstatuses import ShowStatus, ScheduledStatus

# Create your models here.
class Ticket(models.Model, Subject):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name="tickets")
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

    def notify(self, message=""):
        """
        Notify customers about ticket-related updates.
        """
        self.customer.update(message=message)

    @staticmethod
    def cancelled_show(show, message=""):
        """
        Notify all customers who have tickets for the show that the show has been cancelled.
        """
        tickets = Ticket.objects.filter(show=show)
        
        for ticket in tickets:
            ticket.notify(message=f"We regret to inform you that the show has been cancelled, and your ticket with id:{ticket.id} is no longer valid.")

    def cancel(self):
        self.isCancelled = True
        self.save()

    def getShowTimimg(self):
        return (self.show.slot.timing)

    def getShowDate(self):
        return self.show.slot.date
