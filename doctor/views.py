from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from clinic.models import Clinic
from clinic.serializers import ClinicSerializer
from clinic.utils import CustomPageNumberPagination
from .models import Doctor
from .serializers import DoctorDetailSerializer
from .permissions import IsDoctor, IsDoctorOwner


class UpdateDetailDoctorAPIView(generics.RetrieveUpdateAPIView):
    """
    Update detail doctor profile API view.
    Only doctor can access his data and update it.
    """
    permission_classes = [IsDoctor]
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer
    
    def get_object(self, *args, **kwargs):
        # get current doctor user.
        obj = get_object_or_404(Doctor, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorListAPIView(generics.ListAPIView):
    """
    Return list of all doctors.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doctor.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = DoctorDetailSerializer


class DoctorClinicListAPIView(generics.ListAPIView):
    """
    Return list of all clinics of current authenticated doctor.
    Paginate and filter the results by is outdated.
    """
    permission_classes = [IsDoctor]
    serializer_class = ClinicSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the clinics
        for the currently authenticated doctor.
        """
        return Clinic.objects.filter(doctor=self.request.user.doctor)