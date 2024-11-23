from decimal import Decimal
from enum import Enum
from django.core.validators import MinValueValidator
from django.db import models
from users.models import Customer

class TransactionTypes(Enum):
    TICKET_PURCHASED = 0
    TICKET_CANCELLED = 1
    MEMBERSHIP_PURCHASED = 2

    @classmethod
    def choices(cls):
        return [(item.value, item.name.replace('_', ' ').title()) for item in cls]

# Create your models here.
class TransactionHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="transaction_history")
    transaction_type = models.PositiveSmallIntegerField(choices=TransactionTypes.choices(), null=False)
    amount = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=6,
        null=False,
        validators=[MinValueValidator(Decimal('0.00'))]
        )

    created_at = models.DateTimeField(auto_now_add=True)
