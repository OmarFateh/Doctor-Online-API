from django.urls import path

from .views import (ClinicListAPIView, CreateClinicAPIView, DetailUpdateDeleteClinicAPIView,
                    ClinicReservationListAPIView, AddCancelClinicReservationAPIView)


"""
CLIENT
BASE ENDPOINT /api/clinics/
"""

urlpatterns = [
    path('list/', ClinicListAPIView.as_view(), name='clinic-list'),
    path('create/', CreateClinicAPIView.as_view(), name='create-clinic'),
    path('<str:clinic_uuid>/', DetailUpdateDeleteClinicAPIView.as_view(), 
        name='detail-update-delete-clinic'),
    path('<str:clinic_uuid>/reservations/list/', ClinicReservationListAPIView.as_view(), 
        name='clinic-reservation-list'),
    path('<str:clinic_uuid>/reservation/add/cancel/', AddCancelClinicReservationAPIView.as_view(), 
        name='clinic-add-cancel-reservation'),
    
]