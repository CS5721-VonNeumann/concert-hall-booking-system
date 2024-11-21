from rest_framework import serializers
from .memberships import MembershipTypeEnum

class PurchaseMembershipSerializer(serializers.Serializer):
    membership_type = serializers.ChoiceField(
        choices=[code.name for code in MembershipTypeEnum],
        required=True
        )
    membership_period = serializers.IntegerField(min_value=1, required=True)