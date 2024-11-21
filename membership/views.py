import json

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from membership.models import CustomerMembership
from membership.serializers import PurchaseMembershipSerializer
from membership.services import get_membership_factory
from users.middleware import get_current_user
from users.models import Customer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def purchaseMembership(request: HttpRequest):
    data = json.loads(request.body)
    serializer = PurchaseMembershipSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    customer = Customer.objects.get(user=get_current_user())

    factory = get_membership_factory(serializer.data['membership_type'])
    if not factory:
        return JsonResponse(
            {"error": "Invalid membership type"},
            status=HTTP_400_BAD_REQUEST
        )

    membership_instance = factory.create_membership()

    try:
        # Save the membership type to the user's profile
        CustomerMembership.objects.create(
            customer=customer,
            membership_type=membership_instance.get_membership_code(),
            price=membership_instance.get_membership_price(),
            expiry=membership_instance.get_expiry(serializer.data['membership_period'])
        )
        return JsonResponse(
            {"Success": "Membership purchase is Successful"},
            status=HTTP_200_OK
        )
    except Exception as exc:
        return JsonResponse(
            {
                "Faliure": "Membership purchase is unsuccessful.",
                "Error": str(exc)
            },
            status=HTTP_400_BAD_REQUEST
        )
