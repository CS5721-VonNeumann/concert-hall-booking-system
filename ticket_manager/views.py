from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
import json

from .services import is_seat_available, create_ticket

def bookTickets(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        show_id = data.get('show_id')
        seats = data.get('seats')  # Array of seat IDs or numbers
        customer_id = data.get('customer_id')

        if seat_objs := is_seat_available(show_id, seats):
            # TODO: payment gateway
            # pass
            if tickets := create_ticket(customer_id, show_id, seat_objs):
                return JsonResponse({"ticket_ids": list(tickets)})
            return JsonResponse({"error": "Something went wrong creating ticketse."}, status=404)

        return JsonResponse({"error": "Seat not available."}, status=404)
        
    return JsonResponse({"error": "Invalid request method."}, status=405)
