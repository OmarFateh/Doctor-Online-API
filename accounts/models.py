from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts


class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """
    def validate_email_address(self, email):
        """
        Take email and check if it's a valid email.
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('You must provide a valid email address.')

    def validate_password(self, password):
        """
        Take password and check if it's a valid password.
        """
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValueError(e)

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if email:
            email = self.normalize_email(email)
            self.validate_email_address(email)
        else:    
            raise ValueError('Users must have an email address')
        if password:
            self.validate_password(password)
        else:    
            raise ValueError('Users must have a password')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """
        Take email and password, and create superuser.
        """
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True, 
                                is_active=True, user_type="M")    
        return user


class User(AbstractUser):
    """
    Custom user model where email is the unique identifiers
    for authentication instead of username.
    """
    TYPES_CHOICES = (
        ('M', 'Moderator'),
        ('D', 'Doctor'),
        ('P', 'Patient'),
    )

    username = None
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=1, choices=TYPES_CHOICES, default='P')
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # USERNAME_FIELD and password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_moderator(self):
        """Return True if User is Moderator, else False"""
        return self.user_type == 'M'    

    def is_doctor(self):
        """Return True if User is Doctor, else False"""
        return self.user_type == 'D'

    def is_patient(self):
        """Return True if User is Patient, else False"""
        return self.user_type == 'P'