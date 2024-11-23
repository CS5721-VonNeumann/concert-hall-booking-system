from rest_framework import serializers
from .models import Customer, ShowProducer
from django.contrib.auth.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

class CustomerUserSerializer(serializers.ModelSerializer):
    # Define fields that belong to the User model as well
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['email', 'phone', 'password', 'first_name', 'last_name']

    def validate_email(self, value):
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        # Check if phone number is unique and format is valid
        if Customer.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        if not re.match(r'^\+?\d{10,20}$', value):
            raise serializers.ValidationError("Phone number must contain only digits and be 10-20 characters long.")
        return value

    def create(self, validated_data):
        # Extract data for the User model fields
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['email'],  # Set email as username
            email=validated_data['email'],
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create CustomerUser instance linked to User instance
        customer_user = Customer.objects.create(
            user=user,
            phone=validated_data['phone']
        )
        return customer_user

class ShowProducerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()  # Email field
    phone = serializers.CharField(max_length=20)  # Phone field
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    organisation = serializers.CharField(write_only=True)  # Organisation field

    class Meta:
        model = ShowProducer
        fields = ['email', 'phone', 'password', 'first_name', 'last_name', 'organisation']

    def validate_email(self, value):
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        # Check if phone number is unique and format is valid
        if ShowProducer.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        if not re.match(r'^\+?\d{10,20}$', value):
            raise serializers.ValidationError("Phone number must contain only digits and be 10-20 characters long.")
        return value

    def validate_organisation(self, value):
        # Ensure organisation is not empty
        if not value.strip():
            raise serializers.ValidationError("Organisation cannot be blank.")
        return value

    def create(self, validated_data):
        """ Create a user and show producer instance """
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        organisation = validated_data.pop('organisation')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as the username
            email=validated_data['email'],
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create ShowProducer instance linked to User instance
        show_producer = ShowProducer.objects.create(
            user=user,
            phone=validated_data['phone'],
            organisation=organisation
        )
        return show_producer