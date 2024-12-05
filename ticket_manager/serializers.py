from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Ticket
from users.middleware import get_current_user
from show_manager.serializers import ShowSerializer
from .models import Ticket
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
    
class TicketHistorySerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Ticket
            fields = '__all__'

class TicketSalesRequestSerializer(serializers.Serializer):
    show_name = serializers.CharField(required=True)
    slot_id = serializers.IntegerField(required=False)

    def validate(self,data):
        show_name = data.get('show_name')
        slot_id = data.get('slot_id',None)
        try:
            show = Show.objects.filter(
                name=show_name
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError("No show found with the given name")
        if hasattr(get_current_user(), 'showproducer'):
            if not (slot_id):
                raise serializers.ValidationError("For Show Producer, slot_id is required.")
        if slot_id:
            try:
                show = Show.objects.filter(
                    name=show_name,
                    slot_id=slot_id
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError("No show found with the given name and slot")
            except ValueError:
                raise serializers.ValidationError("Invalid Format")
        return data

class TicketSerializer(serializers.ModelSerializer):
    show = ShowSerializer()  
    class Meta:
        model = Ticket
        fields = ['id', 'customer', 'show', 'seat', 'isCancelled']  
