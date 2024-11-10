from django.shortcuts import HttpResponse, get_object_or_404
from django.http import HttpRequest, JsonResponse
from users.models import ShowProducer
from show_manager.services import ShowRequestService
from django.core import serializers
from django.forms.models import model_to_dict
from .models import Slot
from hall_manager.models import Hall
import json

def create_show_request(request: HttpRequest):
    # TODO update logic to get producer
    # show_producer = request.show_producer
    show_producer = get_object_or_404(ShowProducer, id=1)

    body = json.loads(request.body)

    name = body.get('name')
    category = body.get('category')
    has_intermission = body.get('has_intermission')

    slot_id = body.get('slot_id')
    slot = get_object_or_404(Slot, id=slot_id)
    

    hall_id = body.get('hall_id')
    hall = get_object_or_404(Hall, id=hall_id)

    # Use the service to request a show
    show = ShowRequestService.request_show(
        show_producer, 
        name,
        category,
        has_intermission,
        slot,
        hall,
    )
    
    show_dict = model_to_dict(show)
    return JsonResponse(show_dict)