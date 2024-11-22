import json
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import Hall, Venue, Slot, Category, HallSupportsSlot, HallSupportsCategory, Seat
from .seattypes import SeatTypeEnum
from show_manager.models import Show
from django.forms.models import model_to_dict
from django.db.models import F
from users.middleware import get_current_user
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import AddSeatsToHallSerializer, ChangeSeatTypeSerializer

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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_seats_to_hall(request: HttpRequest):
    user = get_current_user()
    if not user.is_superuser:
        return JsonResponse({"error": "Permission denied"}, status=403)
    
    body = json.loads(request.body)

    # Validate input with serializer
    serializer = AddSeatsToHallSerializer(data=body)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    hall = get_object_or_404(Hall, id=validated_data["hall_id"])
    seat_numbers = validated_data["seat_numbers"]

    existing_seats = set(Seat.objects.filter(hall=hall).values_list("seat_number", flat=True))
    new_seat_numbers = [num for num in seat_numbers if num not in existing_seats]

    Seat.objects.bulk_create([
        Seat(seat_number=num, hall=hall) for num in new_seat_numbers
    ])

    if len(new_seat_numbers):
        hall.hall_capacity = F('hall_capacity') + len(new_seat_numbers)
        hall.save()

    return JsonResponse({
        "message": f"Added {len(new_seat_numbers)} seats to hall {hall.hall_name}",
        "existing_seats_skipped": len(seat_numbers) - len(new_seat_numbers),
    }, status=200)

        

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_seat_type(request: HttpRequest):
    user = get_current_user()
    if not user.is_superuser:
        return JsonResponse({"error": "Permission denied"}, status=403)
    
    body = json.loads(request.body)
    # Validate input with serializer
    serializer = ChangeSeatTypeSerializer(data=body)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    hall = get_object_or_404(Hall, id=validated_data["hall_id"])
    seat_updates = validated_data["seat_updates"]

    seat_types = {i.name: i.value for i in SeatTypeEnum}
    invalid_updates = []
    updated_count = 0

    for update in seat_updates:
        seat_number = update.get("seat_number")
        seat_type = update.get("seat_type")

        if not seat_number:
            update['reason'] = "Invalid seat number"
            invalid_updates.append(update)
            continue

        if not seat_type or seat_type not in seat_types:
            update['reason'] = "Invalid seat type"
            invalid_updates.append(update)
            continue

        seat = Seat.objects.filter(hall=hall, seat_number=seat_number).first()
        if seat:
            seat.seat_type = seat_type
            seat.save()
            updated_count += 1
        else:
            update['reason'] = "Seat does not exist"
            invalid_updates.append(update)

    return JsonResponse({
        "message": f"Updated {updated_count} seats in hall {hall.hall_name}",
        "invalid_updates": invalid_updates,
    }, status=200)
    
        
