import json
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import Hall, Venue, Slot, Category, HallSupportsSlot, HallSupportsCategory
from show_manager.models import Show
from django.forms.models import model_to_dict

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

def create_venue(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)

        venue_name = body.get('venue_name')
        location = body.get('location')
        phone_number = body.get('phone_number')

        Venue.objects.create(
            venue_name=venue_name,
            location=location,
            phone_number=phone_number
        )

        return JsonResponse({
                "message": "Venue created successfully",
            }, status=201) 

    return JsonResponse({"error": "Invalid request method."}, status=405)

def create_slot(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)

        date = body.get('date')
        timing = body.get('timing')

        Slot.objects.create(
            date=date,
            timing=timing
        )

        return JsonResponse({
                "message": "Slot created successfully",
            }, status=201) 

    return JsonResponse({"error": "Invalid request method."}, status=405)

def create_category(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        
        category_name = body.get('category_name')

        Category.objects.create(
            category_name=category_name
        )

        return JsonResponse({
                "message": "Category created successfully",
            }, status=201) 
    
    return JsonResponse({"error": "Invalid request method."}, status=405)

def assign_slot_to_hall(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)

        hall_id = body.get('hall_id')
        hall = get_object_or_404(Hall, id=hall_id)
        
        slot_id = body.get('slot_id')
        slot = get_object_or_404(Slot, id=slot_id)
        
        HallSupportsSlot.objects.create(
            hall=hall,
            slot=slot
        )

        return JsonResponse({
                "message": "Slot assigned to hall successfully",
            }, status=201)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)

def assign_category_to_hall(request: HttpRequest):
    if request.method == 'POST':
        body = json.loads(request.body)

        hall_id = body.get('hall_id')
        hall = get_object_or_404(Hall, id=hall_id)
        
        category_id = body.get('category_id')
        category = get_object_or_404(Category, id=category_id)

        HallSupportsCategory.objects.create(
            hall=hall,
            category=category
        )

        return JsonResponse({
                "message": "Category assigned to hall successfully",
            }, status=201)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)

def get_halls(request: HttpRequest):
    if request.method == 'GET':
        try:
            category_id = request.GET.get('category_id')
            category = get_object_or_404(Category, id=category_id)

            slot_id = request.GET.get('slot_id')
            slot = get_object_or_404(Slot, id=slot_id)

            supporting_halls = Hall.get_halls_by_category_and_slot(category=category, slot=slot)
            available_supporting_halls = []
            
            for hall in supporting_halls:
                if not Show.is_overlapping_show_exists(hall=hall, slot=slot):
                    available_supporting_halls.append(model_to_dict(hall))

            return JsonResponse({
                'halls_response': available_supporting_halls
            }, status=200)
        except Exception as e:
            print(e)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)
