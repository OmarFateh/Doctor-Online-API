import datetime

import factory

from clinic.models import Clinic, Reservation
from doctor.tests.factories import DoctorFactory
from patient.tests.factories import PatientFactory


class ClinicFactory(factory.django.DjangoModelFactory):
    """
    Create new clinic instance.
    """
    class Meta:
        model = Clinic
        django_get_or_create = ('uuid',)

    doctor = factory.SubFactory(DoctorFactory)
    uuid = "36e6abc3-6c46-4624-8e29-52340ceaf53b"
    name = 'name'
    price = '500'
    date = datetime.datetime.strptime('24052010', "%d%m%Y").date()
    start_time = datetime.datetime.strptime('24052010', "%d%m%Y").time()
    end_time = '8:00'


class ReservationFactory(factory.django.DjangoModelFactory):
    """
    Create new reservation instance.
    """
    class Meta:
        model = Reservation
        django_get_or_create = ('clinic', 'patient',)

    clinic = factory.SubFactory(ClinicFactory)
    patient = factory.SubFactory(PatientFactory)
    is_active = True