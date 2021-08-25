import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from .factories import PatientUserFactory

register(PatientUserFactory)


@pytest.fixture
def new_patient_user(db, patient_user_factory):
    user = patient_user_factory.create()
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()