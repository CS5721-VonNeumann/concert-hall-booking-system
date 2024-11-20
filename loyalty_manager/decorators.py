from abc import ABC, abstractmethod
from membership.memberships import MembershipCodeEnum

class LoyaltyDecorator(ABC):
    @abstractmethod
    def get_loyalty_points(self):
        pass

class RegularLoyalty(LoyaltyDecorator):
    def get_loyalty_points(self):
        return 10

class MembershipLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, membership_type):
        self.loyalty_decorator = loyalty_decorator
        self.membership_type = membership_type

    def get_loyalty_points(self):
        regular_points = self.loyalty_decorator.get_loyalty_points()

        if self.membership.type == MembershipCodeEnum.GOLD:
            return regular_points + 50
        elif self.membership.type == MembershipCodeEnum.SILVER:
            return regular_points + 25
        return regular_points

class NewCustomerLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer):
        self.loyalty_decorator = loyalty_decorator
        self.customer = customer

    def get_loyalty_points(self):
        regular_points = self.loyalty_decorator.get_loyalty_points()

        if self.customer.is_new:
            return regular_points + 100
        return regular_points
