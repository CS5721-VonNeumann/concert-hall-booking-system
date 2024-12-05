from rest_framework import serializers
from .memberships import MembershipTypeEnum
from .models import CustomerMembership

from rest_framework import serializers
from .models import CustomerMembership

class CustomerMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMembership
        fields = ['id', 'customer', 'membership_type', 'price', 'expiry', 'created_at']

class PurchaseMembershipSerializer(serializers.Serializer):
    membership_type = serializers.ChoiceField(
        choices=[code.name for code in MembershipTypeEnum],
        required=True
        )
    membership_period = serializers.IntegerField(min_value=1, required=True)

class MembershipPurchaseHistorySerializer(serializers.ModelSerializer):
    
        class Meta:
            model = CustomerMembership
            fields = '__all__'