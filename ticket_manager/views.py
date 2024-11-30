import json

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from payment_gateway.facade import PaymentGatewayFacade
from users.middleware import get_current_user
from users.models import Customer
from membership.models import CustomerMembership
from .serializers import BookTicketSerializer
from .services import return_available_seats, create_ticket

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bookTickets(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())
    customer_membership = CustomerMembership.objects.filter(customer=customer).first()

    data = json.loads(request.body)

    serializer = BookTicketSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data

    if seat_objs := return_available_seats(validated_data['show_obj'], validated_data['seats']):

        payment_gateway = PaymentGatewayFacade()

        if bill_amount := payment_gateway.get_ticket_bill_amount(customer, seat_objs):
            if tickets := create_ticket(customer, validated_data['show_obj'], seat_objs):
                
                create_transaction(customer, TransactionTypes.TICKET_PURCHASED, bill_amount)
                customer_membership.calculate_loyalty_points()
                
                return JsonResponse({
                    "ticket_ids": list(tickets),
                    "total_amount": bill_amount
                    }, status=HTTP_200_OK)
        
            return JsonResponse({"error": "Something went wrong creating tickets."}, status=HTTP_404_NOT_FOUND)
        
        return JsonResponse({"error": "Payment Failed."}, status=HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Seat not available."}, status=HTTP_404_NOT_FOUND)
