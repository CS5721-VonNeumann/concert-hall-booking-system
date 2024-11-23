from membership.factories import (
    GoldMembershipFactory,
    RegularMembershipFactory,
    SilverMembershipFactory
    )
from membership.memberships import MembershipTypeEnum


def get_membership_factory(membership_type):

    #get factory based on membership type
    if membership_type == MembershipTypeEnum.REGULAR.name:
        return RegularMembershipFactory()
    elif membership_type == MembershipTypeEnum.SILVER.name:
        return SilverMembershipFactory()
    elif membership_type == MembershipTypeEnum.GOLD.name:
        return GoldMembershipFactory()
    else:
        return None
    