import factory

from accounts.models import User


class PatientUserFactory(factory.django.DjangoModelFactory):
    """
    Create new patient user instance.
    """
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'P'


class DoctorUserFactory(factory.django.DjangoModelFactory):
    """
    Create new doctor user instance.
    """
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail1@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'D'


class ModeratorUserFactory(factory.django.DjangoModelFactory):
    """
    Create new moderator user instance.
    """
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail2@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'M'