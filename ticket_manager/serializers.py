from django.shortcuts import get_object_or_404
from rest_framework import serializers

from show_manager.models import Show

class BookTicketSerializer(serializers.Serializer):

    show_id = serializers.IntegerField(required=True)
    seats = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
        )
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        show_id = attrs.get('show_id')
        seat_list = attrs.get('seats')

        show_obj = get_object_or_404(Show, id=show_id)

        if any(seat > show_obj.hall.hall_capacity for seat in seat_list):
            raise serializers.ValidationError({"seats":"Some of the requested seats do not exist in the hall."})
        
        attrs['show_obj'] = show_obj

        return attrs