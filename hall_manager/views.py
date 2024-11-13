import json

from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import Hall, Venue

def create_hall(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)

        hall_name = body.get('hall_name')
        hall_capacity = body.get('hall_capacity')

        venue_id = body.get('venue_id')
        venue = get_object_or_404(Venue, id=venue_id)

        Hall.objects.create(
            hall_name=hall_name,
            hall_capacity = hall_capacity,
            venue = venue,
        )

        return JsonResponse({
                "message": "Hall created successfully",
            }, status=201) 

    return JsonResponse({"error": "Invalid request method."}, status=405)

def create_slot():
    print("TEST")

def create_venue():
    print("TEST")