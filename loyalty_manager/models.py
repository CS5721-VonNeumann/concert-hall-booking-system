from django.db import models
from django.utils.timezone import now

from users.models import Customer
from loyalty_manager.decorators import MembershipLoyaltyDecorator, NewCustomerLoyaltyDecorator, RegularLoyalty

class CustomerLoyalty(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customerloyalties")
    loyalty_points = models.IntegerField(default=0)

    def calculate_loyalty_points(self):
        # customers with expired memberships will have zero loyalty points
        if self.expiry < now():
            self.loyalty_points = 0
            self.save()
            return 0

        regular_loyalty = RegularLoyalty()

        loyalty_with_membership = MembershipLoyaltyDecorator(regular_loyalty, self.membership_type)

        total_loyalty = NewCustomerLoyaltyDecorator(loyalty_with_membership, self.customer)

        return total_loyalty.get_loyalty_points()
