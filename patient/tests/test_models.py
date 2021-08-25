import pytest


class TestModel:

    def test_patient_str(self, new_patient):
        """
        Test patient obj str method.
        """
        assert new_patient.__str__() == 'testemail@gmail.com'