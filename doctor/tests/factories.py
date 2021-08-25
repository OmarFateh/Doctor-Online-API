import factory

from doctor.models import Doctor
from accounts.tests.factories import DoctorUserFactory


class DoctorFactory(factory.django.DjangoModelFactory):
    """
    Create new doctor instance.
    """
    class Meta:
        model = Doctor
        django_get_or_create = ('user',)

    user = factory.SubFactory(DoctorUserFactory)
    info = 'info'
    specialization = 'specialization'