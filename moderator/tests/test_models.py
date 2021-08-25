import pytest


class TestModel:

    def test_moderator_str(self, new_moderator):
        """
        Test moderator obj str method.
        """
        assert new_moderator.__str__() == 'testemail2@gmail.com'