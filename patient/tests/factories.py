import factory

from patient.models import Patient
from accounts.tests.factories import PatientUserFactory


class PatientFactory(factory.django.DjangoModelFactory):
    """
    Create new patient instance.
    """
    class Meta:
        model = Patient
        django_get_or_create = ('user',)

    user = factory.SubFactory(PatientUserFactory)
    gender = 'M'
    phone = '+999999999'
    birthdate = '2021-11-10'