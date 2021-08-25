import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import DoctorUserFactory, PatientUserFactory
from patient.tests.factories import PatientFactory
from .factories import ClinicFactory, ReservationFactory

register(DoctorUserFactory)
register(PatientUserFactory)
register(PatientFactory)
register(ClinicFactory)
register(ReservationFactory)


@pytest.fixture
def new_doctor_user(db, doctor_user_factory):
    doctor = doctor_user_factory.create()
    return doctor


@pytest.fixture
def new_patient_user(db, patient_user_factory):
    patient = patient_user_factory.create()
    return patient


@pytest.fixture
def new_patient(db, patient_factory):
    patient = patient_factory.create()
    return patient


@pytest.fixture
def new_clinic(db, clinic_factory):
    clinic = clinic_factory.create()
    return clinic


@pytest.fixture
def new_reservation(db, reservation_factory):
    reservation = reservation_factory.create()
    return reservation


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()