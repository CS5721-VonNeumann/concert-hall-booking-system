from abc import ABC, abstractmethod
from ticket_manager.models import Ticket

class LoyaltyDecorator(ABC):
    @abstractmethod
    def get_loyalty_points(self):
        pass

class RegularLoyalty(LoyaltyDecorator):
    def get_loyalty_points(self):
        return 10

class MembershipLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer_membership):
        self.loyalty_decorator = loyalty_decorator
        self.customer_membership = customer_membership

    def get_loyalty_points(self):
        loyalty_points = self.loyalty_decorator.get_loyalty_points()
        membership_type_class = self.customer_membership.get_membership_type_class()

        loyalty_booster = membership_type_class.get_loyalty_booster()

        total_loyalty_points = loyalty_points * loyalty_booster
        return total_loyalty_points

class NewCustomerLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer):
        self.loyalty_decorator = loyalty_decorator
        self.customer = customer

    def get_loyalty_points(self):
        loyalty_points = self.loyalty_decorator.get_loyalty_points()
        is_new_customer = not Ticket.is_issued_to_customer(self.customer)

        if is_new_customer:
            return loyalty_points * 1.25
        return loyalty_points
