from django.urls import path

from .views import (RegisterDoctorAPIView, RegisterPatientAPIView, LoginUserAPIView,
                    ChangePassowordAPIView)


"""
CLIENT
BASE ENDPOINT /api/users/
"""

urlpatterns = [
    # Authentication
    path('register/doctor/', RegisterDoctorAPIView.as_view(), name='register-doctor'),
    path('register/patient/', RegisterPatientAPIView.as_view(), name='register-patient'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    # Password
    path('password/change/', ChangePassowordAPIView.as_view(), name='password-change'),
]