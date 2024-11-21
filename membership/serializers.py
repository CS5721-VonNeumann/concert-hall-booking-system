from rest_framework import serializers
from .memberships import MembershipCodeEnum

class PurchaseMembershipSerializer(serializers.Serializer):
    membership_code = serializers.ChoiceField(
        choices=[code.name for code in MembershipCodeEnum],
        required=True
        )
    membership_period = serializers.IntegerField(min_value=1, required=True)