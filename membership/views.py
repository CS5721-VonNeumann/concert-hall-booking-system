import json

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from membership.models import CustomerMembership
from membership.serializers import PurchaseMembershipSerializer
from membership.services import get_membership_factory
from payment_gateway.facade import PaymentGatewayFacade
from payment_gateway.models import TransactionTypes
from payment_gateway.services import create_transaction
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
        payment_gateway = PaymentGatewayFacade()
        if bill_amount := payment_gateway.get_membership_bill_amount(membership_instance.get_membership_price()):
            # Save the membership type to the user's profile
            CustomerMembership.objects.create(
                customer=customer,
                membership_type=membership_instance.get_membership_type(),
                price=membership_instance.get_membership_price(),
                expiry=membership_instance.get_expiry(serializer.data['membership_period'])
            )
            create_transaction(customer, TransactionTypes.MEMBERSHIP_PURCHASED, bill_amount)

            return JsonResponse(
                {
                    "Amount": bill_amount,
                    "Success": "Membership purchase is Successful"
                },
                status=HTTP_200_OK
            )
        return JsonResponse(
                {
                    "Failure": "Membership amount not found.",
                },
                status=HTTP_400_BAD_REQUEST
            )
    except Exception as exc:
        return JsonResponse(
            {
                "Failure": "Membership purchase is unsuccessful.",
                "Error": str(exc)
            },
            status=HTTP_400_BAD_REQUEST
        )
