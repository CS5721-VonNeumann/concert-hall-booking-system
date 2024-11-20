import json

from datetime import datetime, timedelta, timezone
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from membership.models import CustomerMembership
from membership.services import get_membership_factory
from users.middleware import get_current_user
from users.models import Customer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def purchaseMembership(request: HttpRequest):
    data = json.loads(request.body)
    membership_type = data.get('membership_type')
    customer = Customer.objects.get(user=get_current_user())

    factory = get_membership_factory(membership_type)
    if not factory:
        return JsonResponse(
            {"error": "Invalid membership type"},
            status=HTTP_400_BAD_REQUEST
        )
    
    membership_instance = factory.create_membership()

    # Define membership expiration (temp. 1-year duration)
    expiry_date = datetime.now(timezone.utc) + timedelta(membership_instance.get_expiry())

    # Save the membership type to the user's profile
    user_membership = CustomerMembership.objects.update_or_create(
        customer = customer,
        membership_type =  membership_instance.get_membership_type(),
        price = membership_instance.get_membership_price(),
        expiry = expiry_date,
    )

    return JsonResponse(
        {"Success": "Membership purchase is Successful"},
        status=HTTP_200_OK
    )