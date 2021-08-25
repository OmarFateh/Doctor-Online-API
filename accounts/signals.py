from django.dispatch import receiver
from django.db.models.signals import post_save

from patient.models import Patient
from doctor.models import Doctor
from moderator.models import Moderator
from .models import User


@receiver(post_save, sender=User)     
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create an empty profile for each user type once the user is added.
    """
    if created:
        if instance.user_type == 'M':
            Moderator.objects.create(user=instance)
        elif instance.user_type == 'D':   
            Doctor.objects.create(user=instance)
        elif instance.user_type == 'P':    
            Patient.objects.create(user=instance)