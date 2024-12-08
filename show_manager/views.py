import json
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpRequest
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from users.middleware import get_current_user
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from config.utils import get_query_param_schema

from .models import Show, ShowStatusEnum, ShowProducer
from users.models import ShowProducer
from ticket_manager.models import Ticket
from .serializers import CreateShowRequestSerializer, UpdateScheduledShowRequestSerializer, CancelShowRequestSerializer, CancelShowSerializer, ShowSerializer
from .services import ShowRequestService

from .constants import PERMISSION_DENIED_ERROR

@swagger_auto_schema(
    request_body=CreateShowRequestSerializer,
    method='POST'
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_update_show_request(request: HttpRequest):
    show_producer = ShowProducer.objects.get(user=get_current_user())

    body = json.loads(request.body)
    # Validate input with serializer
    serializer =CreateShowRequestSerializer(data=body, show_producer=show_producer)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    name = validated_data['name']
    category = validated_data['category']
    has_intermission = validated_data['has_intermission']
    slot = validated_data['slot']
    hall = validated_data['hall']

    show_id = validated_data.get('show_id', None)

    # Use the service to request a show
    show = ShowRequestService.request_show(
        show_id,
        show_producer, 
        name,
        category,
        has_intermission,
        slot,
        hall,
    )
    
    return JsonResponse({
        'show_response': model_to_dict(show)
    })

@swagger_auto_schema(
    request_body=UpdateScheduledShowRequestSerializer,
    method='POST'
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_scheduled_show(request: HttpRequest):
    show_producer = ShowProducer.objects.get(user=get_current_user())

    body = json.loads(request.body)
    # Validate input with serializer
    serializer = UpdateScheduledShowRequestSerializer(data=body, show_producer=show_producer)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    show = validated_data['show']
    name = validated_data['name']
    has_intermission = validated_data['has_intermission']

    # Use the service to request a show
    show.name = name
    show.has_intermission = has_intermission
    show.save()

    return JsonResponse({
        'show_response': model_to_dict(show)
    })

@swagger_auto_schema(
    request_body=CancelShowRequestSerializer,
    method='PUT'
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def cancel_show_request(request):
    """
    Cancel a show request by updating its status.
    """
    show_producer = ShowProducer.objects.get(user=get_current_user())

    body = json.loads(request.body)
    # Validate input with serializer
    serializer = CancelShowRequestSerializer(data=body, show_producer=show_producer)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    show = validated_data['show']
    show.cancel()

    return Response({"message": "Show canceled successfully."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    request_body=CancelShowSerializer,
    method='PUT'
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def cancel_show(request):
    admin_user = get_current_user().is_superuser

    if not admin_user:
        return JsonResponse({"error": PERMISSION_DENIED_ERROR}, status=403)
    
    body = json.loads(request.body)
    # Validate input with serializer
    serializer = CancelShowSerializer(data=body, admin_user=admin_user)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    show: Show = validated_data['show']

    message = f"The Show: {show.name} has been cancelled. Sorry for the inconvenience"
    show.cancel(message=message)
    Ticket.cancelled_show(show=show, message=message)

    return Response({"message": "Show canceled successfully."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    manual_parameters=[
        get_query_param_schema("page", required=False),
        get_query_param_schema("limit", required=False)
    ],
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_show_requests(request):
    """
    List all show requests made by the authenticated show producer.
    """
    show_producer = ShowProducer.objects.get(user=get_current_user())
    page = request.query_params.get("page", 1)
    limit = request.query_params.get("limit", 10)

    # Filter and paginate results
    shows = Show.objects.filter(show_producer=show_producer).order_by("-id")
    paginator = Paginator(shows, limit)
    page_obj = paginator.get_page(page)

    serializer = ShowSerializer(page_obj, many=True)
    return Response({
        "results": serializer.data,
        "total": paginator.count,
        "pages": paginator.num_pages,
        "current_page": page_obj.number,
    })

@swagger_auto_schema(
    manual_parameters=[
        get_query_param_schema("page", required=False),
        get_query_param_schema("limit", required=False)
    ],
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_scheduled_shows(request):
    """
    Fetch and return all scheduled shows for customwers
    """
    user = get_current_user()
    is_customer = hasattr(user, 'customer')

    if is_customer:
        shows = Show.objects.filter(status=ShowStatusEnum.SCHEDULED.name)
    else:
        return JsonResponse({"error": PERMISSION_DENIED_ERROR}, status=403)

    page = request.query_params.get("page", 1)
    limit = request.query_params.get("limit", 10)

    paginator = Paginator(shows, limit)
    page_obj = paginator.get_page(page)
    
    serializer = ShowSerializer(page_obj, many=True)
    return Response({
        "results": serializer.data,
        "total": paginator.count,
        "pages": paginator.num_pages,
        "current_page": page_obj.number,
    })

@swagger_auto_schema(
    manual_parameters=[
        get_query_param_schema("page", required=False),
        get_query_param_schema("limit", required=False)
    ],
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_shows(request):
    """
    Fetch and return all shows
    """
    user = get_current_user()
    is_admin = user.is_superuser

    if is_admin:
        shows = Show.objects.all()
    else:
        return JsonResponse({"error": "Permission denied"}, status=403)

    page = request.query_params.get("page", 1)
    limit = request.query_params.get("limit", 10)

    paginator = Paginator(shows, limit)
    page_obj = paginator.get_page(page)
    
    serializer = ShowSerializer(page_obj, many=True)
    return Response({
        "results": serializer.data,
        "total": paginator.count,
        "pages": paginator.num_pages,
        "current_page": page_obj.number,
    })