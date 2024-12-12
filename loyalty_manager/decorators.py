from abc import ABC, abstractmethod
from users.models import Customer
from membership.memberships import Membership

# Abstract base class defining the interface for loyalty decorators
class LoyaltyDecorator(ABC):
    @abstractmethod
    def get_loyalty_points(self):
        # method to compute loyalty points.
        pass

# Concrete implementation for regular loyalty points
class RegularLoyalty(LoyaltyDecorator):
    def get_loyalty_points(self):
        return 10

class NewCustomerLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer: Customer):
        self.loyalty_decorator = loyalty_decorator
        self.customer = customer

    def get_loyalty_points(self):
        loyalty_points = self.loyalty_decorator.get_loyalty_points()
        is_new_customer = self.customer.loyalty_points == 0
        
        if is_new_customer:
            return loyalty_points * 1.25

        return loyalty_points

class MembershipLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer_membership: Membership):
        self.loyalty_decorator = loyalty_decorator
        self.customer_membership = customer_membership

    def get_loyalty_points(self):
        loyalty_points = self.loyalty_decorator.get_loyalty_points()
        loyalty_booster = self.customer_membership.get_loyalty_booster()

        total_loyalty_points = loyalty_points * loyalty_booster
        return total_loyalty_points