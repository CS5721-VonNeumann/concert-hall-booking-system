import json

from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Hall, Slot, Category, HallSupportsSlot, HallSupportsCategory, Seat
from show_manager.models import Show
from .serializers import HallSerializer, VenueSerializer, SlotSerializer, CategorySerializer, AddSeatsToHallSerializer, ChangeSeatTypeSerializer
from .seattypes import SeatTypeEnum
from config.utils import get_query_param_schema
from users.middleware import get_current_user

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_hall(request: HttpRequest):
    serializer = HallSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Hall created successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_venue(request: HttpRequest):
    serializer = VenueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Venue created successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_slot(request: HttpRequest):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Slot created successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request: HttpRequest):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Category created successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_slot_to_hall(request: HttpRequest):
    body = request.data

    hall_id = body.get('hall_id')
    slot_id = body.get('slot_id')

    hall = get_object_or_404(Hall, id=hall_id)
    slot = get_object_or_404(Slot, id=slot_id)

    # Create the relationship
    HallSupportsSlot.objects.create(hall=hall, slot=slot)

    return JsonResponse({"message": "Slot assigned to hall successfully"}, status=201)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_category_to_hall(request: HttpRequest):
    body = request.data

    hall_id = body.get('hall_id')
    category_id = body.get('category_id')

    hall = get_object_or_404(Hall, id=hall_id)
    category = get_object_or_404(Category, id=category_id)

    # Create the relationship
    HallSupportsCategory.objects.create(hall=hall, category=category)

    return JsonResponse({"message": "Category assigned to hall successfully"}, status=201)

@swagger_auto_schema(
    manual_parameters=[
        get_query_param_schema("category_id", required=False),
        get_query_param_schema("slot_id", required=False)
    ],
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_halls(request: HttpRequest):
    try:
        category_id = request.GET.get('category_id')
        slot_id = request.GET.get('slot_id')

        category = get_object_or_404(Category, id=category_id)
        slot = get_object_or_404(Slot, id=slot_id)

        # Get supporting halls
        supporting_halls = Hall.get_halls_by_category_and_slot(category=category, slot=slot)
        available_supporting_halls = []

        for hall in supporting_halls:
            if not Show.is_overlapping_show_exists(hall=hall, slot=slot):
                available_supporting_halls.append(HallSerializer(hall).data)

        return JsonResponse({'halls_response': available_supporting_halls}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

@swagger_auto_schema(
    request_body=AddSeatsToHallSerializer,
    method='PUT'
)
@api_view(["PUT"])
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

        
@swagger_auto_schema(
    request_body=ChangeSeatTypeSerializer,
    method='PUT'
)
@api_view(["PUT"])
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