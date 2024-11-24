from django.utils.timezone import now
from django.db import models
from users.models import Customer
from membership.memberships import (
    GoldMembership, 
    MembershipTypeEnum, 
    SilverMembership,
    RegularMembership
) 

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
