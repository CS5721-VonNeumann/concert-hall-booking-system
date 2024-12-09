from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from membership.serializers import CustomerMembershipSerializer
from .serializer import CustomerUserSerializer, ShowProducerSerializer,LoginSerializer
from config.logger import logger
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    request_body=CustomerUserSerializer,
    method='POST'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_customer(request):
    customer_serializer = CustomerUserSerializer(data=request.data)

    if customer_serializer.is_valid():
        try:
            # Save the user and customer data
            customer_user = customer_serializer.save()

            customer_membership_data = {
                "customer": customer_user.id, 
                "membership_type": "REGULAR", 
                "price": 0.0, 
                "expiry": None
            }
            # Validate and save CustomerMembership
            customer_membership_serializer = CustomerMembershipSerializer(data=customer_membership_data)

            if customer_membership_serializer.is_valid():
                customer_membership_serializer.save()
            else:
                return Response(
                    customer_membership_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            token, created = Token.objects.get_or_create(user=customer_user.user)
            # Generate token for the created user
            logger.info(f"Customer registered with id {customer_user.user.email}")
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"error": "An unexpected error occurred while registering the customer."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # If the data is invalid, return a 400 response with errors
    logger.error(customer_serializer.errors)
    return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    request_body=ShowProducerSerializer,
    method='POST'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_showproducer(request):
    serializer = ShowProducerSerializer(data=request.data)
    # Validate the incoming data
    if serializer.is_valid():
        try:
            show_producer = serializer.save()
            # Create a token for the user associated with this show producer
            token, created = Token.objects.get_or_create(user=show_producer.user)
            logger.info(f"ShowProducer registered with id {show_producer.user.email}")
            return Response({"message": "Show producer registered successfully.", "token": token.key}, status=status.HTTP_201_CREATED)

        except Exception:
            return Response({"error": "An unexpected error occurred while registering the show producer."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    logger.error(serializer.errors)
    # Return validation errors if the data is invalid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

@swagger_auto_schema(
    request_body=LoginSerializer,
    method='POST'
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    # Use the serializer for validation
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    # Authenticate the user
    user = authenticate(username=email, password=password)
    if user is None:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        # Check if user is a Customer or ShowProducer
        if hasattr(user, 'customer'):
            profile = 'Customer'
        elif hasattr(user, 'showproducer'):
            profile = 'ShowProducer'
        else:
            return Response({"error": "User does not have a valid profile"}, status=status.HTTP_400_BAD_REQUEST)

        Token.objects.filter(user=user).delete()
        # Get or create the token for the user
        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f"User with ID {user.email} signed in")
        return Response({
            "token": token.key,
            "user_id": user.id,
            "email": user.email,
            "profile_type": profile
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(
    request_body=LoginSerializer,
    method='POST'
)
@api_view(["POST"])
@permission_classes([AllowAny])
def admin_login(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        # Authenticate the user
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the authenticated user is an admin
        if not user.is_superuser:  # `is_superuser` is used to check if the user has admin privileges
            return Response({"error": "User is not authorized as an admin"}, status=status.HTTP_403_FORBIDDEN)

        Token.objects.filter(user=user).delete()
        # Get or create an authentication token
        token, _ = Token.objects.get_or_create(user=user)
        logger.info("Admin logged in")
        # Return the token and data
        return Response({
        "message": "Admin logged in",
        "token": token.key
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        