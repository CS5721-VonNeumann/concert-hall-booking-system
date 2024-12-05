import json
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from config.utils import get_query_param_schema
from payment_gateway.facade import PaymentGatewayFacade
from users.middleware import get_current_user
from users.models import Customer
from membership.models import CustomerMembership
from .serializers import BookTicketSerializer
from .models import Ticket
from .serializers import BookTicketSerializer, TicketHistorySerializer
from .serializers import BookTicketSerializer, TicketSalesRequestSerializer,TicketSerializer
from .services import return_available_seats, create_ticket
from .ticketsalestrategy import AdminTicketSalesStrategy,ShowProducerTicketSalesStrategy,TicketSalesContext


@swagger_auto_schema(
    request_body=BookTicketSerializer,
    method='POST'
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bookTickets(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())
    customer_membership = CustomerMembership.objects.filter(customer=customer).first()
    latest_valid_membership = customer_membership.get_latest_valid_membership_instance(customer=customer)

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

                customer_membership.calculate_loyalty_points(customer=customer, latest_valid_membership=latest_valid_membership)

                return JsonResponse({
                    "ticket_ids": list(tickets),
                    "total_amount": bill_amount
                }, status=HTTP_200_OK)

            return JsonResponse({"error": "Something went wrong creating tickets."}, status=HTTP_404_NOT_FOUND)

        return JsonResponse({"error": "Payment Failed."}, status=HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Seat not available."}, status=HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    manual_parameters=[
        get_query_param_schema("page", required=False),
        get_query_param_schema("limit", required=False)
    ],
    method='GET'
)
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
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def view_ticket_sales(request):
    user = get_current_user()
    serializer = TicketSalesRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)
    
    data = serializer.validated_data
    show_name = data["show_name"]
    slot_id = data.get("slot_id", None)

    try:
        if user.is_superuser:
            strategy = AdminTicketSalesStrategy()
        elif hasattr(user, 'showproducer'):
            strategy = ShowProducerTicketSalesStrategy()
        else:
            return JsonResponse({"error": "Unauthorized access"}, status=403)

        context = TicketSalesContext(strategy)
        ticket_sales = context.fetch_sales(show_name, slot_id)
        serialized_sales = TicketSerializer(ticket_sales, many=True).data

        return JsonResponse(serialized_sales, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
