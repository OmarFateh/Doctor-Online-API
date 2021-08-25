from rest_framework import generics, permissions, status
from rest_framework.response import Response

from doctor.models import Doctor
from doctor.serializers import DoctorCreateSerializer
from patient.models import Patient
from patient.serializers import PatientCreateSerializer
from .models import User
from .permissions import AnonPermissionOnly
from .serializers import UserLoginSerializer, PassowordChangeSerializer


class RegisterDoctorAPIView(generics.CreateAPIView):
    """
    User registeration and profile creation API view.
    """
    permission_classes = [AnonPermissionOnly]
    queryset = Doctor.objects.all()
    serializer_class = DoctorCreateSerializer


class RegisterPatientAPIView(generics.CreateAPIView):
    """
    User registeration and profile creation API view.
    """
    permission_classes = [AnonPermissionOnly]
    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer


class LoginUserAPIView(generics.GenericAPIView):
    """
    User login API view.
    """
    permission_classes = [AnonPermissionOnly]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassowordAPIView(generics.UpdateAPIView):
    """
    User profile update API view.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PassowordChangeSerializer

    def update(self, request, *args, **kwargs):
        """
        Override the update method and update user's password.
        """
        serializer = PassowordChangeSerializer(
            request.user, data=request.data, partial=True, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"success": "Your password was changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)