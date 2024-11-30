from django.utils.timezone import now
from django.db import models
from users.models import Customer
from membership.memberships import (
    GoldMembership, 
    MembershipTypeEnum, 
    SilverMembership,
    RegularMembership
)
from loyalty_manager.decorators import MembershipLoyaltyDecorator, NewCustomerLoyaltyDecorator, RegularLoyalty

class CustomerMembership(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customermemberships")
    membership_type = models.CharField(max_length=10)
    price = models.FloatField(default=0)
    expiry = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def get_membership_type_class(self):
        if self.membership_type == MembershipTypeEnum.REGULAR.name:
            return RegularMembership()
        elif self.membership_type == MembershipTypeEnum.SILVER.name:
            return SilverMembership()
        elif self.membership_type == MembershipTypeEnum.GOLD.name:
            return GoldMembership()
        else:
            return None
        
    def calculate_loyalty_points(self):
        latest_valid_membership = self.get_latest_valid_membership(self.customer)

        # If the customer has no active membership, no loyalty points calculated
        if not latest_valid_membership:
            return

        regular_loyalty = RegularLoyalty()

        new_customer_loyalty = NewCustomerLoyaltyDecorator(regular_loyalty, self.customer)
        
        loyalty_with_membership = MembershipLoyaltyDecorator(new_customer_loyalty, latest_valid_membership)

        total_loyalty_points = loyalty_with_membership.get_loyalty_points()
        self.customer.loyalty_points = total_loyalty_points
        self.customer.save()

    @staticmethod
    def get_latest_valid_membership_instance(customer):
    # Filter memberships by expiry date and order by expiry descending
        latest_membership = (
            customer.customermemberships.filter(expiry__gt=now())  # Filter memberships whose expiry is in the future
            .order_by('-expiry')  # Order by expiry descending to get the latest first
            .first()
        )

        if latest_membership:
            return latest_membership.get_membership_type_class()
        else:
            return RegularMembership()
