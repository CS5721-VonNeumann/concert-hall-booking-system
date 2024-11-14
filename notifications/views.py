from django.shortcuts import get_object_or_404
from django.http import HttpRequest, JsonResponse
from users.models import ShowProducer
from django.forms.models import model_to_dict
import json
from .models import ShowProducerNotifications
from users.middleware import get_current_user
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_show_producer_notifications(request: HttpRequest):
    if request.method == 'GET':
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
    
    return JsonResponse({"error": "Invalid request method."}, status=405)



def mark_show_producer_notifications_as_read(request: HttpRequest, notification_id: int):
    if request.method == 'POST':
        # Retrieve the notification by ID
        notification = ShowProducerNotifications.objects.get(id=notification_id)
        
        # Mark the notification as read
        notification.isRead = True
        notification.save()
        
        return JsonResponse({'message': 'Notification marked as read successfully'}, status=200)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)