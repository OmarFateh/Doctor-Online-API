from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from clinic.serializers import PatientReservationSerializer
from clinic.utils import CustomPageNumberPagination
from clinic.models import Reservation
from .permissions import IsPatient
from .serializers import PatientDetailSerializer
from .models import Patient


class UpdateDetailPatientAPIView(generics.RetrieveUpdateAPIView):
    """
    Update detail patient profile API view.
    Only patient can access his data and update it.
    """
    permission_classes = [IsPatient]
    queryset = Patient.objects.all()
    serializer_class = PatientDetailSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
    
    def get_object(self, *args, **kwargs):
        # get current patient user.
        obj = get_object_or_404(Patient, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class PatientClinicReservationListAPIView(generics.ListAPIView):
    """
    Return list of all active reservations of current patient.
    """
    permission_classes = [IsPatient]
    serializer_class = PatientReservationSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all active clinics reservations
        for the currently authenticated patient.
        """
        return Reservation.objects.filter(patient=self.request.user.patient, is_active=True)