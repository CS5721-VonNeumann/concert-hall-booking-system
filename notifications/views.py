from django.http import HttpRequest, JsonResponse
from users.models import ShowProducer, Customer
from django.forms.models import model_to_dict
from .models import ShowProducerNotifications, CustomerNotifications
from users.middleware import get_current_user
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_show_producer_notifications(request: HttpRequest):
    show_producer = ShowProducer.objects.get(user=get_current_user())

    # Filter notifications where the show_producer matches the given ID and is unread
    unread_notifications = ShowProducerNotifications.objects.filter(show_producer=show_producer, isRead=False)
    
    # # Serialize notifications to a list of dictionaries
    notifications = []
    for notification in unread_notifications:
        notifications.append(model_to_dict(notification))

    return JsonResponse({
        'notifications_response': notifications
    }, status=200)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_show_producer_notifications_as_read(request: HttpRequest, notification_id: int):
    # Retrieve the notification by ID
    notification = ShowProducerNotifications.objects.filter(id=notification_id).first()
    
    if not notification:
        return JsonResponse({
            'error': "Invalid notification ID"
        }, status=HTTP_404_NOT_FOUND)
    
    # Mark the notification as read
    notification.isRead = True
    notification.save()
    
    return JsonResponse({'message': 'Notification marked as read successfully'}, status=200)

@swagger_auto_schema(
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_customer_notifications(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())

    print(customer.id)

    # Filter notifications where the customer matches the given ID and is unread
    unread_notifications = CustomerNotifications.objects.filter(customer=customer, isRead=0)
    
    # Serialize notifications to a list of dictionaries
    notifications = []
    for notification in unread_notifications:
        notifications.append(model_to_dict(notification))

    return JsonResponse({
        'notifications_response': notifications
    }, status=200)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_customer_notifications_as_read(request: HttpRequest, notification_id: int):
    # Retrieve the notification by ID
    notification = CustomerNotifications.objects.filter(id=notification_id).first()
    
    if not notification:
        return JsonResponse({
            'error': "Invalid notification ID"
        }, status=HTTP_404_NOT_FOUND)
    
    # Mark the notification as read
    notification.isRead = True
    notification.save()
    
    return JsonResponse({'message': 'Notification marked as read successfully'}, status=200)
