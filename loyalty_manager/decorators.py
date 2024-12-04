from abc import ABC, abstractmethod
from ticket_manager.models import Ticket
from membership.memberships import Membership

class LoyaltyDecorator(ABC):
    @abstractmethod
    def get_loyalty_points(self):
        pass

class RegularLoyalty(LoyaltyDecorator):
    def get_loyalty_points(self):
        return 10

class MembershipLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer_membership: Membership):
        self.loyalty_decorator = loyalty_decorator
        self.customer_membership = customer_membership

    def get_loyalty_points(self):
        loyalty_points = self.loyalty_decorator.get_loyalty_points()
        loyalty_booster = self.customer_membership.get_loyalty_booster()

        total_loyalty_points = loyalty_points * loyalty_booster
        return total_loyalty_points

class NewCustomerLoyaltyDecorator(LoyaltyDecorator):
    def __init__(self, loyalty_decorator: LoyaltyDecorator, customer):
        self.loyalty_decorator = loyalty_decorator
        self.customer = customer

    def get_loyalty_points(self):
        loyalty_points = self.loyalty_decorator.get_loyalty_points()
        
        ticket_count = Ticket.objects.filter(customer=self.customer).count()
        
        if ticket_count == 0:
            return loyalty_points * 1.25

        return loyalty_points
