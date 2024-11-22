from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from payment_gateway.models import TransactionHistory
from payment_gateway.serializers import TransactionHistorySerializer
from users.middleware import get_current_user
from users.models import Customer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_transaction_history(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())

    transactions = TransactionHistory.objects.filter(customer=customer).order_by('-created_at')

    serializer = TransactionHistorySerializer(transactions, many=True)

    return Response(serializer.data, status= HTTP_200_OK)

