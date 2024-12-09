from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from users.middleware import get_current_user
from users.middleware import get_current_user
from .models import Ticket
from users.middleware import get_current_user
from show_manager.serializers import ShowSerializer
from .models import Ticket
from show_manager.models import Show
from show_manager.showstatuses import ShowStatusEnum
from .services import is_ticket_cancellation_allowed

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
        if show_obj.status != ShowStatusEnum.SCHEDULED.name:
            raise serializers.ValidationError("Ticket cannot be booked for a non-scheduled show.")

        if any(seat > show_obj.hall.hall_capacity for seat in seat_list):
            raise serializers.ValidationError({"seats":"Some of the requested seats do not exist in the hall."})
        
        attrs['show_obj'] = show_obj

        return attrs
    
class TicketHistorySerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Ticket
            fields = '__all__'
class TicketCancellationSerializer(serializers.Serializer):
    ticket_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={"required": "Ticket IDs are required.", "blank": "Ticket IDs cannot be empty."}
    )

    def validate_ticket_ids(self, ticket_ids):
        """
        Validate that each ticket exists, belongs to the customer, and meets cancellation rules.
        """
        user = get_current_user()  # Make sure the user is being fetched correctly
        # Check if the user is a customer
        if not hasattr(user, 'customer'):
            raise serializers.ValidationError("The logged-in user is not a customer.")

        customer = user.customer
        validated_tickets = []

        for ticket_id in ticket_ids:
            try:
                ticket = Ticket.objects.get(id=ticket_id, customer=customer)
            except Ticket.DoesNotExist:
                raise serializers.ValidationError(f"Invalid ticket ID {ticket_id} or the ticket does not belong to you.")

            # Check if the ticket is already canceled
            if ticket.isCancelled:
                raise serializers.ValidationError(f"Ticket ID {ticket_id} is already canceled.")

            # Check if ticket cancellation is allowed
            if not is_ticket_cancellation_allowed(ticket_id, customer):
                raise serializers.ValidationError(f"Cancellation not allowed for Ticket ID {ticket_id} within current membership rules.")

            validated_tickets.append(ticket.id)

        # Save the validated tickets for further use
        self.context["validated_tickets"] = validated_tickets
        return ticket_ids

class TicketSalesRequestSerializer(serializers.Serializer):
    show_name = serializers.CharField(required=True)
    slot_id = serializers.IntegerField(required=False)

    def validate(self, data):
        show_name = data.get('show_name')
        slot_id = data.get('slot_id',None)
        try:
            Show.objects.get(
                name=show_name
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError("No show found with the given name")
        if hasattr(get_current_user(), 'showproducer') and not (slot_id):
            raise serializers.ValidationError("For Show Producer, slot_id is required.")
        if slot_id:
            try:
                Show.objects.filter(
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
