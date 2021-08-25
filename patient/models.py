from django.db import models
from django.core.validators import RegexValidator

from moderator.models import BaseTimestamp


class Patient(BaseTimestamp):
    """
    Patient model with OneToOne relation with custom user model.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField("accounts.user", on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    phone = models.CharField(max_length=16, validators=[
        RegexValidator(regex=r'^\+\d{9,15}$', code='invalid_phone',
        message="Phone number must be entered in the format: '+999999999'.Up to 15 digits allowed.")
    ])
    birthdate = models.DateField(null=True)

    def __str__ (self):
        """
        Return patient's email.
        """
        return self.user.email
