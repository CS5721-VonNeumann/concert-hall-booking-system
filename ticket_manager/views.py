import json

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.middleware import get_current_user
from users.models import Customer
from .services import return_available_seats, create_ticket

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bookTickets(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())

    data = json.loads(request.body)
    show_id = data.get('show_id')
    seats = data.get('seats')  # Array of seat IDs or numbers

    if seat_objs := return_available_seats(show_id, seats):
        # TODO: payment gateway
        if tickets := create_ticket(customer, show_id, seat_objs):
            return JsonResponse({"ticket_ids": list(tickets)})
        return JsonResponse({"error": "Something went wrong creating tickets."}, status=400)

    return JsonResponse({"error": "Seat not available."}, status=404)
