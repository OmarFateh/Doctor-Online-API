import pytest


class TestClinicModel:

    def test_clinic_str(self, new_clinic):
        """
        Test clinic obj str method.
        """
        assert new_clinic.__str__() == 'name | testemail1@gmail.com'

    def test_clinic_is_outdated(self, new_clinic):
        """
        Test clinic obj is outdated method.
        """
        assert new_clinic.is_outdated == True


class TestReservationModel:
    
    def test_reservation_str(self, new_reservation):
        """
        Test reservation obj str method.
        """
        assert new_reservation.__str__() == 'name | testemail@gmail.com'