import json
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from config.utils import get_query_param_schema
from membership.models import CustomerMembership
from membership.serializers import PurchaseMembershipSerializer, MembershipPurchaseHistorySerializer
from membership.services import get_membership_factory
from payment_gateway.facade import PaymentGatewayFacade
from users.middleware import get_current_user
from users.models import Customer


@swagger_auto_schema(
    request_body=PurchaseMembershipSerializer,
    method='POST'
)
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
    

@swagger_auto_schema(
    manual_parameters=[
        get_query_param_schema("page", required=False),
        get_query_param_schema("limit", required=False)
    ],
    method='GET'
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_membership_history(request: HttpRequest):
    customer = Customer.objects.get(user=get_current_user())
    page = request.query_params.get("page", 1)
    limit = request.query_params.get("limit", 10)

    memberships = CustomerMembership.objects.filter(customer=customer).order_by('-created_at')
    paginator = Paginator(memberships, limit)
    page_obj = paginator.get_page(page)

    serializer = MembershipPurchaseHistorySerializer(page_obj, many=True)

    return Response(serializer.data, status= HTTP_200_OK)
