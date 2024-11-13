import json

from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import Hall, Venue, Slot

def create_hall(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)

        hall_name = body.get('hall_name')
        hall_capacity = body.get('hall_capacity')

        venue_id = body.get('venue_id')
        venue = get_object_or_404(Venue, id=venue_id)

        slot_id = body.get('slot_id')
        slot = get_object_or_404(Slot, id=slot_id)

        Hall.objects.create(
            hall_name=hall_name,
            hall_capacity = hall_capacity,
            venue = venue,
            slot = slot
        )

        return JsonResponse({
                "message": "Hall created successfully",
            }, status=201) 

    return JsonResponse({"error": "Invalid request method."}, status=405)