from django.urls import path

from .views import UpdateDetailDoctorAPIView, DoctorListAPIView, DoctorClinicListAPIView


"""
CLIENT
BASE ENDPOINT /api/doctors/
"""

urlpatterns = [
    path('my-profile/', UpdateDetailDoctorAPIView.as_view(), name='doctor-profile-detail-update'),
    path('list/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('my-clinics/list/', DoctorClinicListAPIView.as_view(), name='doctor-clinic-list')
]