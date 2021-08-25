import uuid
from datetime import datetime

from django.db import models

from doctor.models import Doctor
from moderator.models import BaseTimestamp


class Clinic(BaseTimestamp):
    """
    Clinic model.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    doctor = models.ForeignKey("doctor.doctor", related_name='clinics', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField("Clinic Date")
    start_time = models.TimeField("Clinic Start Time")
    end_time = models.TimeField("Clinic End Time")

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        """
        Return clinic's name & doctor's email.
        """
        return f"{self.name} | {self.doctor.user.email}"

    @property
    def is_outdated(self):
        """
        Return true if the date and start time of clinic has passed.
        """
        today = datetime.today()
        day = datetime.combine(self.date, self.start_time)
        return day <= today 


class Reservation(BaseTimestamp):
    """
    Clinic Reservation model.
    """
    clinic = models.ForeignKey(Clinic, related_name='reservations', on_delete=models.CASCADE)
    patient = models.ForeignKey("patient.patient", related_name='reservations', 
                            on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        unique_together = ['clinic', 'patient']

    def __str__(self):
        """
        Return clinic's name & patient's email.
        """
        return f"{self.clinic.name} | {self.patient.user.email}"    
