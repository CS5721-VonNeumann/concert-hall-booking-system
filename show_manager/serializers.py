from rest_framework import serializers

from .models import Show, Slot, Hall, Category
from .showstatuses import ScheduledStatus, PendingStatus

from .constants import (
    SHOW_NOT_FOUND_ERROR,
    INVALID_SCHEDULED_STATUS_ERROR,
    INVALID_PENDING_STATUS_ERROR,
    NO_ACCESS_TO_UPDATE_ERROR,
    NO_ACCESS_TO_CANCEL_ERROR,
)

class CreateShowRequestSerializer(serializers.Serializer):
    show_id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    category_id = serializers.IntegerField()
    has_intermission = serializers.BooleanField()
    slot_id = serializers.IntegerField()
    hall_id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        # Accept `show_producer` as a context parameter
        self.show_producer = kwargs.pop('show_producer', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        # Validate category existence
        category_id = data.get("category_id")
        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError("Invalid category ID.")
        
        data['category'] = Category.objects.filter(id=category_id).first()

        # Validate slot existence
        slot_id = data.get("slot_id")
        if not Slot.objects.filter(id=slot_id).exists():
            raise serializers.ValidationError("Invalid slot ID.")
        
        data['slot'] = Slot.objects.filter(id=slot_id).first()

        # Validate hall existence
        hall_id = data.get("hall_id")
        if not Hall.objects.filter(id=hall_id).exists():
            raise serializers.ValidationError("Invalid hall ID.")
        
        data['hall'] = Hall.objects.filter(id=hall_id).first()

        show_id = data.get('show_id')
        if show_id:
            if not Show.objects.filter(id=show_id).exists():
                raise serializers.ValidationError("Invalid show ID.")
            show = Show.objects.filter(id=show_id).first()
            if not isinstance(show.get_status_instance(), PendingStatus):
                raise serializers.ValidationError(INVALID_PENDING_STATUS_ERROR)
            if show.show_producer != self.show_producer:
                raise serializers.ValidationError(NO_ACCESS_TO_UPDATE_ERROR)

        return data


class UpdateScheduledShowRequestSerializer(serializers.Serializer):
    show_id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    has_intermission = serializers.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        # Accept `show_producer` as a context parameter
        self.show_producer = kwargs.pop('show_producer', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        # Validate show existence
        show_id = data.get("show_id")
        show = Show.objects.filter(id=show_id).first()
        if not show:
            raise serializers.ValidationError(SHOW_NOT_FOUND_ERROR)
        data['show'] = show

        if not isinstance(show.get_status_instance(), ScheduledStatus):
            raise serializers.ValidationError(INVALID_SCHEDULED_STATUS_ERROR)
        
        if show.show_producer != self.show_producer:
            raise serializers.ValidationError(NO_ACCESS_TO_UPDATE_ERROR)

        return data

class CancelShowRequestSerializer(serializers.Serializer):
    show_id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        # Accept `show_producer` as a context parameter
        self.show_producer = kwargs.pop('show_producer', None)
        super().__init__(*args, **kwargs)


    def validate(self, data):
        # Validate show existence
        show_id = data.get("show_id")
        show = Show.objects.filter(id=show_id).first()
        if not show:
            raise serializers.ValidationError(SHOW_NOT_FOUND_ERROR)
        data['show'] = show

        if not isinstance(show.get_status_instance(), PendingStatus):
            raise serializers.ValidationError(INVALID_PENDING_STATUS_ERROR)
        
        if show.show_producer != self.show_producer:
            raise serializers.ValidationError(NO_ACCESS_TO_CANCEL_ERROR)

        return data

class CancelShowSerializer(serializers.Serializer):
    show_id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        # Accept `admin` as a context parameter
        self.admin_user = kwargs.pop('admin_user', None)
        super().__init__(*args, **kwargs)


    def validate(self, data):
        # Validate show existence
        show_id = data.get("show_id")
        show = Show.objects.filter(id=show_id).first()
        if not show:
            raise serializers.ValidationError(SHOW_NOT_FOUND_ERROR)
        data['show'] = show

        if not isinstance(show.get_status_instance(), ScheduledStatus):
            raise serializers.ValidationError(INVALID_SCHEDULED_STATUS_ERROR)
        
        if not self.admin_user:
            raise serializers.ValidationError(NO_ACCESS_TO_CANCEL_ERROR)

        return data

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'name', 'category', 'has_intermission', 'slot', 'hall', 'status']
