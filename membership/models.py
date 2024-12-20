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
    membership_type = models.CharField(max_length=10, default=MembershipTypeEnum.REGULAR.name)
    price = models.FloatField(default=0.0)
    expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_membership_type_class(self):
        if self.membership_type == MembershipTypeEnum.REGULAR.name:
            return RegularMembership()
        elif self.membership_type == MembershipTypeEnum.SILVER.name:
            return SilverMembership()
        elif self.membership_type == MembershipTypeEnum.GOLD.name:
            return GoldMembership()
        return None

    def calculate_loyalty_points(self, customer, latest_valid_membership):
        if not latest_valid_membership:
            return
        
        existing_loyalty_points = customer.loyalty_points or 0

        regular_loyalty = RegularLoyalty()
        new_customer_loyalty = NewCustomerLoyaltyDecorator(regular_loyalty, customer)
        loyalty_with_membership = MembershipLoyaltyDecorator(new_customer_loyalty, latest_valid_membership)

        calculated_loyalty_points = loyalty_with_membership.get_loyalty_points()

        total_loyalty_points = existing_loyalty_points + calculated_loyalty_points
        customer.loyalty_points = total_loyalty_points
        customer.save()

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
        return RegularMembership()