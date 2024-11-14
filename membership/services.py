from membership.factories import (
    GoldMembershipFactory,
    RegularMembershipFactory,
    SilverMembershipFactory
    )
from membership.memberships import MembershipCodeEnum


def get_membership_factory(membership_type):

    #get factory based on membership type
    if membership_type == MembershipCodeEnum.REGULAR.name:
        return RegularMembershipFactory()
    elif membership_type == MembershipCodeEnum.SILVER.name:
        return SilverMembershipFactory()
    elif membership_type == MembershipCodeEnum.GOLD.name:
        return GoldMembershipFactory()
    else:
        return None
    