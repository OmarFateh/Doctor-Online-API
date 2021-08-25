from django.urls import path

from .views import UpdateDetailPatientAPIView, PatientClinicReservationListAPIView


"""
CLIENT
BASE ENDPOINT /api/patients/
"""

urlpatterns = [
    path('my-profile/', UpdateDetailPatientAPIView.as_view(), name='patient-profile-detail-update'),
    path('my-reservations/list/', PatientClinicReservationListAPIView.as_view(), 
          name='patient-reservation-list'),
]