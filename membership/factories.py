from abc import ABC,abstractmethod
from membership.memberships import RegularMembership,SilverMembership,GoldMembership

#define factory
class MembershipFactory(ABC):
    @abstractmethod
    def create_membership(self):
        pass

#define Concrete factory

class RegularMembershipFactory(MembershipFactory):
    def create_membership(self):
        return RegularMembership()


class SilverMembershipFactory(MembershipFactory):
    def create_membership(self):
        return SilverMembership()


class GoldMembershipFactory(MembershipFactory):
    def create_membership(self):
        return GoldMembership()