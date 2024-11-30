import json
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from payment_gateway.facade import PaymentGatewayFacade
from users.middleware import get_current_user
from users.models import Customer
from .models import Ticket
from .serializers import BookTicketSerializer, TicketHistorySerializer
from .services import return_available_seats, create_ticket

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bookTickets(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())
    data = json.loads(request.body)

    serializer = BookTicketSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data

    if seat_objs := return_available_seats(validated_data['show_obj'], validated_data['seats']):

        payment_gateway = PaymentGatewayFacade()
        price_per_ticket, bill_amount = payment_gateway.get_ticket_bill_amount(
            customer, seat_objs)

        if bill_amount:

            if tickets := create_ticket(customer, validated_data['show_obj'], seat_objs, price_per_ticket):

                return JsonResponse({
                    "ticket_ids": list(tickets),
                    "total_amount": bill_amount
                }, status=HTTP_200_OK)

            return JsonResponse({"error": "Something went wrong creating tickets."}, status=HTTP_404_NOT_FOUND)

        return JsonResponse({"error": "Payment Failed."}, status=HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Seat not available."}, status=HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ticket_history(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())
    page = request.query_params.get("page", 1)
    limit = request.query_params.get("limit", 10)

    tickets = Ticket.objects.filter(
        customer=customer).order_by('-updated_at', '-id')
    paginator = Paginator(tickets, limit)
    page_obj = paginator.get_page(page)

    serializer = TicketHistorySerializer(page_obj, many=True)

    return Response(serializer.data, status=HTTP_200_OK)
