import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import DoctorUserFactory
from clinic.tests.factories import ClinicFactory
from .factories import DoctorFactory

register(DoctorUserFactory)
register(ClinicFactory)
register(DoctorFactory)


@pytest.fixture
def new_doctor_user(db, doctor_user_factory):
    doctor = doctor_user_factory.create()
    return doctor


@pytest.fixture
def new_doctor(db, doctor_factory):
    doctor = doctor_factory.create()
    return doctor


@pytest.fixture
def new_clinic(db, clinic_factory):
    clinic = clinic_factory.create()
    return clinic


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()