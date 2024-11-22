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
from .serializers import BookTicketSerializer, TicketHistorySerializer,TicketCancellationSerializer
from .services import return_available_seats, create_ticket
from .template import CustomerTicketView
from .command import CancelTicketCommand, RefundCommand
from users.middleware import get_current_user
from users.models import Customer
from .services import return_available_seats, create_ticket,TicketCommandControl,isTicketCancellationAllowed
from .models import Ticket
from django.core.exceptions import ValidationError

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_view_tickets(request):
    try:
        customer_view = CustomerTicketView()
        response_data = customer_view.process_request(get_current_user())
        serialized_tickets = []
        for ticket in response_data:
            serialized_ticket = {
                "show": ticket.show.name,  
                "venue":ticket.seat.hall.hall_name ,
                "date": ticket.getShowDate(),
                "time": ticket.getShowTimimg()
            }
            serialized_tickets.append(serialized_ticket)
        
        return JsonResponse(serialized_tickets, safe=False)  

    except PermissionError as e:
        return JsonResponse({"error": str(e)}, status=403)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_ticket(request):
    user = get_current_user()
    if not hasattr(user, 'customer'):
        return Response({"error": "The logged-in user is not a customer."}, status=403)
    
    customer = user.customer
    serializer = TicketCancellationSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        tickets = serializer.context["validated_tickets"]
        try:
            # Create the command objects
            cancelCommand = CancelTicketCommand(ticket_ids=tickets, customer=customer)
            refundCommand = RefundCommand(ticket_ids=tickets, customer=customer)

            # Execute the service
            service = TicketCommandControl(
                cancel_command=cancelCommand,
                refund_command=refundCommand
            )
            canceled_tickets = service.execute()
            # Return a success response
            return Response({
                "status": "success",
                "tickets": [ticket.id for ticket in canceled_tickets[0]],
                "message": f"Successfully canceled {len(canceled_tickets[0])} ticket(s).{canceled_tickets[1]}"
            }, status=200)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=400)

    # If validation fails
    return Response({"status": "error", "errors": serializer.errors}, status=400)
