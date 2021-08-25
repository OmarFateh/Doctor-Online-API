import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import PatientUserFactory
from clinic.tests.factories import ReservationFactory
from .factories import PatientFactory

register(PatientUserFactory)
register(ReservationFactory)
register(PatientFactory)


@pytest.fixture
def new_patient_user(db, patient_user_factory):
    patient = patient_user_factory.create()
    return patient


@pytest.fixture
def new_patient(db, patient_factory):
    patient = patient_factory.create()
    return patient


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