from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for user registeration.
    """
    email2 = serializers.EmailField(label='Confirm Email', write_only=True)
    password2 = serializers.CharField(label='Confirm Password', 
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'email2', 
            'password', 'password2']
        extra_kwargs = {"password": {'write_only': True}}

    def validate_password(self, value):
        """
        Validate that password meet django auth validators.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({'password':e})
        return value      

    def validate(self, data):
        """
        Validate that the two emails match.
        Validate that the two passwords match.
        """
        email1 = data.get('email')
        email2 = data.get('email2')
        # check if the two emails match.
        if email1 != email2:
            raise serializers.ValidationError({'email':'The two Emails must match.'})
        # check if the two passwords match.
        password1 = data.get('password')
        password2 = data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError({'password':'The two Passwords must match.'})
        return data

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        user_type = self.context['user_type']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User.objects.create_user(email=email, password=password,
                        first_name=first_name, last_name=last_name, user_type=user_type)
        return user_obj


class UserLoginSerializer(serializers.ModelSerializer):
    """
    A serializer for user login.
    """
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        extra_kwargs = {"password": {'write_only': True}}

    def get_token(self, obj):
        user = User.objects.get(email=obj['email'])
        refresh = RefreshToken.for_user(user)
        response = {'refresh': str(refresh), 'access': str(
            refresh.access_token), }
        return response

    def validate(self, data):
        """
        Validate that entered email and password are correct.
        """
        user = authenticate(**data)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account is not active')
        return data


class PassowordChangeSerializer(serializers.ModelSerializer):
    """
    A serializer for password change.
    """
    old_password = serializers.CharField(label='Old Password', write_only=True)
    new_password1 = serializers.CharField(
        label='New Password', write_only=True)
    new_password2 = serializers.CharField(
        label='Confirm New Password', write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def validate_old_password(self, value):
        """
        Validate that the old password is correct.
        """
        request = self.context['request']
        if not request.user.check_password(value):
            raise serializers.ValidationError("Password is incorrect.")
        return value

    def validate_new_password1(self, value):
        """
        Validate that the two passwords match.
        """
        data = self.get_initial()
        password1 = value
        password2 = data.get('new_password2')
        if password1 != password2:
            raise serializers.ValidationError('The two Passwords must match.')
        return value

    def update(self, instance, validated_data):
        """
        Update user's password.
        """
        password = validated_data['new_password1']
        instance.set_password(password)
        instance.save()
        return validated_data