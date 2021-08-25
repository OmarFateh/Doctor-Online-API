import pytest
from pytest_factoryboy import register

from .factories import ModeratorFactory

register(ModeratorFactory)


@pytest.fixture
def new_moderator(db, moderator_factory):
    moderator = moderator_factory.create()
    return moderator