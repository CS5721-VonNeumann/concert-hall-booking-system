from rest_framework import serializers
from payment_gateway .models import TransactionHistory, TransactionTypes

class TransactionHistorySerializer(serializers.ModelSerializer):
    transaction_type = serializers.SerializerMethodField()
    amount = serializers.DecimalField(max_digits=6, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = TransactionHistory
        fields = '__all__'

    def get_transaction_type(self, obj):
        # Map the transaction_type integer value to its corresponding enum label
        return TransactionTypes(obj.transaction_type).name
