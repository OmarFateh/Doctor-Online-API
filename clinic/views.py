from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from doctor.permissions import IsDoctor, IsDoctorOwner, IsDoctorOwnerOrReadOnly
from patient.models import Patient
from patient.permissions import IsPatient
from .models import Clinic, Reservation
from .utils import CustomPageNumberPagination
from .serializers import ClinicSerializer, ClinicListSerializer, ClinicReservationSerializer


class ClinicListAPIView(generics.ListAPIView):
    """
    Return list of all clinics.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Clinic.objects.select_related('doctor')
    pagination_class = CustomPageNumberPagination
    serializer_class = ClinicListSerializer


class CreateClinicAPIView(generics.CreateAPIView):
    """
    Create new clinic API view.
    Only authenticated doctors can create one.
    """
    permission_classes = [IsDoctor]
    queryset = Clinic.objects.select_related('doctor')
    serializer_class = ClinicSerializer

    def perform_create(self, serializer):
        """
        Set authenticated doctor to be the clinics's doctor automatically.
        """
        serializer.save(doctor=self.request.user.doctor)
    

class DetailUpdateDeleteClinicAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Clinic detail update delete API view.
    Only the authenticated doctor of this clinic can update or delete it.
    """
    permission_classes = [IsDoctorOwnerOrReadOnly]
    queryset = Clinic.objects.select_related('doctor')
    serializer_class = ClinicSerializer

    def get_object(self, *args, **kwargs):
        # get clinic uuid from the requested url.
        clinic_uuid = self.kwargs.get("clinic_uuid", None)
        obj = get_object_or_404(Clinic, uuid=clinic_uuid)
        self.check_object_permissions(self.request, obj)
        return obj


class ClinicReservationListAPIView(generics.ListAPIView):
    """
    Return list of all active reservations for a clinic of current doctor.
    """
    permission_classes = [IsDoctorOwner]
    serializer_class = ClinicReservationSerializer
    pagination_class = CustomPageNumberPagination

    def get_object(self, *args, **kwargs):
        # get clinic uuid from the requested url.
        clinic_uuid = self.kwargs.get("clinic_uuid", None)
        obj = get_object_or_404(Clinic, uuid=clinic_uuid)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all active reservations for this clinic.
        """
        return Reservation.objects.filter(clinic=self.get_object(), is_active=True)  


class AddCancelClinicReservationAPIView(APIView):
    """
    Add or cancel clinic reservation API view.
    Only an authenticated patient can add/cancel it.
    A reservation set to be inactive if the patient cancel it.
    """
    permission_classes = [IsPatient]

    def get_object(self, *args, **kwargs):
        # get clinic uuid from the requested url.
        clinic_uuid = self.kwargs.get("clinic_uuid", None)
        obj = get_object_or_404(Clinic, uuid=clinic_uuid)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def post(self, request, *args, **kwargs):
        """
        Add or cancel a clinic reservation.
        """
        reservation_qs = Reservation.objects.filter(patient=request.user.patient, clinic=self.get_object())
        if reservation_qs.exists():
            reservation_obj = reservation_qs.first()
            if reservation_obj.is_active:
                reservation_obj.is_active = False
                reservation_obj.save()
                return Response({'success':'Your reservation was canceled successfully.'}, 
                                status=status.HTTP_200_OK)
            else:
                reservation_obj.is_active = True
                reservation_obj.save()
                return Response({'success':'Your reservation was added successfully.'}, 
                                status=status.HTTP_200_OK)
        else:    
            Reservation.objects.create(patient=request.user.patient, clinic=self.get_object())
            return Response({'success':'Your reservation was added successfully.'}, 
                            status=status.HTTP_200_OK)    
