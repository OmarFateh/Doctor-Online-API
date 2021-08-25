import pytest


class TestModel:

    def test_doctor_str(self, new_doctor):
        """
        Test doctor obj str method.
        """
        assert new_doctor.__str__() == 'testemail1@gmail.com'