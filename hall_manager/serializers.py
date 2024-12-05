from rest_framework import serializers
from .models import Hall, Slot, Category, Venue, SeatTypeEnum

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'date', 'timing']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'venue_name', 'location', 'phone_number']

class HallSerializer(serializers.ModelSerializer):
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = Hall
        fields = ['id', 'hall_name', 'hall_capacity', 'venue']

class AddSeatsToHallSerializer(serializers.Serializer):
    hall_id = serializers.IntegerField()
    seat_numbers = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False
    )

    def validate_hall_id(self, value):
        if not Hall.objects.filter(id=value).exists():
            raise serializers.ValidationError("Hall with the given ID does not exist.")
        return value

class ChangeSeatTypeSerializer(serializers.Serializer):
    hall_id = serializers.IntegerField()
    seat_updates = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        allow_empty=False
    )

    def validate(self, data):
        # Validate hall existence
        hall_id = data.get("hall_id")
        if not Hall.objects.filter(id=hall_id).exists():
            raise serializers.ValidationError("Hall with the given ID does not exist.")

        # Validate seat updates
        seat_types = {seat_type.name for seat_type in SeatTypeEnum}
        for update in data["seat_updates"]:
            if "seat_number" not in update:
                raise serializers.ValidationError("Each update must have a valid seat_number.")
            if "seat_type" not in update or update["seat_type"] not in seat_types:
                raise serializers.ValidationError(f"Invalid seat_type. Allowed values are: {seat_types}.")

        return data

