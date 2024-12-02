import pytest
import json
from .models import Show, ShowStatusEnum
from hall_manager.models import Category, HallSupportsCategory

@pytest.mark.django_db
def test_raise_request_creates_pending_show(setup_data):

    client = setup_data["client"]
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    request_data = {
        "name": "Test Show",
        "category_id": category.id,
        "has_intermission": True,
        "slot_id": slot.id,
        "hall_id": hall.id
    }

    response = client.post('/shows/raise-request', request_data, format="json")

    assert response.status_code == 200
    show_id = json.loads(response.content.decode())['show_response']['id']
    show = Show.objects.filter(id=show_id).first()
    assert show.name == request_data['name']
    assert show.category == category
    assert show.slot == slot
    assert show.hall == hall
    assert show.show_producer == show_producer


@pytest.mark.django_db
def test_update_show_request(setup_data):
    client = setup_data["client"]
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    category2 = Category.objects.create(category_name='Drama')
    HallSupportsCategory.objects.create(hall=hall, category=category2)

    show_obj = Show.objects.create(name="Test Show", 
                                   category=category, 
                                   hall=hall, 
                                   slot=slot,
                                   has_intermission=True,
                                   show_producer=show_producer
                                   )
    
    request_data = {
        "show_id": show_obj.id,
        "name": show_obj.name,
        "category_id": category2.id,
        "has_intermission": True,
        "slot_id": slot.id,
        "hall_id": hall.id
    }
    
    response = response = client.post('/shows/raise-request', request_data, format="json")

    assert response.status_code == 200
    show = Show.objects.filter(id=show_obj.id).first()
    assert show.name == request_data['name']
    assert show.category == category2
    assert show.slot == slot
    assert show.hall == hall
    assert show.show_producer == show_producer

    show_obj.status = ShowStatusEnum.SCHEDULED.name
    show_obj.save()

    response = client.post('/shows/raise-request', request_data, format="json")
    assert response.status_code == 400
    error_messages = json.loads(response.content.decode())['non_field_errors']
    assert error_messages == ['Show is not in pending status.']

    request_data['show_id'] = 100000

    response = client.post('/shows/raise-request', request_data, format="json")
    assert response.status_code == 400
    error_messages = json.loads(response.content.decode())['non_field_errors']
    assert error_messages == ['Invalid show ID.']

    update_request_data = {
        'show_id': show_obj.id,
        'name': "New Test Name",
        'has_intermission': False
    }

    response = response = client.post('/shows/update-scheduled-show', update_request_data, format="json")

    assert response.status_code == 200
    show = Show.objects.filter(id=show_obj.id).first()
    assert show.name == update_request_data['name']
    assert show.has_intermission == update_request_data["has_intermission"]


@pytest.mark.django_db
def test_cancel_show_request(setup_data):
    client = setup_data["client"]
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    show_obj = Show.objects.create(name="Test Show", 
                                   category=category, 
                                   hall=hall, 
                                   slot=slot,
                                   status=ShowStatusEnum.SCHEDULED.name,
                                   has_intermission=True,
                                   show_producer=show_producer
                                   )
    
    
    request_data = {
        "show_id": show_obj.id,
    }
    
    response = response = client.delete('/shows/cancel-request', request_data, format="json")

    assert response.status_code == 400
    error_messages = json.loads(response.content.decode())['non_field_errors']
    assert error_messages == ['Show is not in pending status.']

    show_obj.status = ShowStatusEnum.PENDING.name
    show_obj.save()

    response = response = client.delete('/shows/cancel-request', request_data, format="json")

    assert response.status_code == 200
    show = Show.objects.filter(id=show_obj.id).first()
    assert show.status == ShowStatusEnum.CANCELLED.name
    

@pytest.mark.django_db
def test_list_requests(setup_data):
    client = setup_data["client"]
    show_producer = setup_data["show_producer"]
    category = setup_data["category"]
    slot = setup_data["slot"]
    hall = setup_data["hall"]

    show_obj = Show.objects.create(name="Test Show", 
                                   category=category, 
                                   hall=hall, 
                                   slot=slot, 
                                   status=ShowStatusEnum.PENDING,
                                   has_intermission=True,
                                   show_producer=show_producer
                                   )
    
    response = client.get('/shows/list-requests')

    assert response.status_code == 200
    response =  json.loads(response.content.decode())
    assert "results" in response
    results = response["results"]
    assert len(results) >= 1
    show = list(filter(lambda req: req['id'] == show_obj.id, results))[0]
    assert show['id'] == show_obj.id
    assert show['name'] == show_obj.name
    assert show['category'] == show_obj.category.id
    assert show['slot'] == show_obj.slot.id
    assert show['hall'] == show_obj.hall.id