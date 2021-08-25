import factory

from moderator.models import Moderator
from accounts.tests.factories import ModeratorUserFactory


class ModeratorFactory(factory.django.DjangoModelFactory):
    """
    Create new moderator instance.
    """
    class Meta:
        model = Moderator
        django_get_or_create = ('user',)

    user = factory.SubFactory(ModeratorUserFactory)