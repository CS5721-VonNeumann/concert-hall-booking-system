from django.http import JsonResponse
from .models import Hall
import json

# Create your views here.

def create_hall(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        hall_name = data.get('hall_name')
        hall_capacity = data.get('hall_capacity', 0)
        hall = Hall.objects.create(
            hall_name=hall_name,
            hall_capacity = hall_capacity
        )
        return JsonResponse({
                "message": "Hall created successfully",
                "hall_id": hall.id,
                "hall_name": hall.hall_name,
                "hall_capacity": hall.hall_capacity,
            }, status=201) 

    return JsonResponse({"error": "Invalid request method."}, status=405)