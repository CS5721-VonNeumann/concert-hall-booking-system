from abc import ABC,abstractmethod
from enum import Enum

#Defining Abstarct Product
class Membership(ABC):

    @abstractmethod
    def get_membership_type(self):
        pass

    @abstractmethod
    def get_membership_price(self):
        pass

    @abstractmethod
    def get_ticket_discount_percentage(self):
        pass

    @abstractmethod
    def get_loyalty_booster(self):
        pass

    @abstractmethod
    def get_refund_percentage(self):
        pass

    @abstractmethod
    def get_cancellation_time_policy(self):
        pass
    
    @abstractmethod
    def get_expiry(self):
        pass


#Defining Concrete product

class RegularMembership(Membership):
    def get_membership_type(self):
        return MembershipCodeEnum.REGULAR.name
    
    def get_membership_price(self):
        return 0  
    
    def get_ticket_discount_percentage(self):
        return 0  

    def get_loyalty_booster(self):
        return 1.0  # No boost for regular

    def get_refund_percentage(self):
        return 50  

    def get_cancellation_time_policy(self):
        return 24

    def get_expiry(self):
        return 365



class SilverMembership(Membership):
    def get_membership_type(self):
        return MembershipCodeEnum.SILVER.name
    
    def get_membership_price(self):
        return 100
    
    def get_ticket_discount_percentage(self):
        return 10

    def get_loyalty_booster(self):
        return 1.2

    def get_refund_percentage(self):
        return 75

    def get_cancellation_time_policy(self):
        return 12

    def get_expiry(self):
        return 365
    

class GoldMembership(Membership):
    def get_membership_type(self):
        return MembershipCodeEnum.GOLD.name
    
    def get_membership_price(self):
        return 300
    
    def get_ticket_discount_percentage(self):
        return 15

    def get_loyalty_booster(self):
        return 1.5

    def get_refund_percentage(self):
        return 90

    def get_cancellation_time_policy(self):
        return 0

    def get_expiry(self):
        return 365


class MembershipCodeEnum(Enum):
    REGULAR = 'REGULAR',
    SILVER = 'SILVER',
    GOLD = 'GOLD'
