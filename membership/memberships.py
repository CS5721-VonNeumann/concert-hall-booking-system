from abc import ABC, abstractmethod
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from enum import Enum

# Defining Abstarct Product
class Membership(ABC):

    @abstractmethod
    def get_membership_code(self):
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
    def get_expiry(self, membership_period):
        pass

# Defining Concrete product

class RegularMembership(Membership):
    def get_membership_code(self):
        return MembershipTypeEnum.REGULAR.name

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

    def get_expiry(self, membership_period):
        return datetime.now(timezone.utc) + relativedelta(months=membership_period)


class SilverMembership(Membership):
    def get_membership_code(self):
        return MembershipTypeEnum.SILVER.name

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

    def get_expiry(self, membership_period):
        return datetime.now(timezone.utc) + relativedelta(months=membership_period)


class GoldMembership(Membership):
    def get_membership_code(self):
        return MembershipTypeEnum.GOLD.name

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

    def get_expiry(self, membership_period):
        return datetime.now(timezone.utc) + relativedelta(months=membership_period)


class MembershipTypeEnum(Enum):
    REGULAR = 'REGULAR',
    SILVER = 'SILVER',
    GOLD = 'GOLD'
