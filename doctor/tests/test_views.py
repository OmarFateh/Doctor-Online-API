import json

from django.urls import reverse


class TestUpdateDetailDoctor:

    data = {'first_name': 'test name'}
    url = reverse('doctors-api:doctor-profile-detail-update')

    def test_doctor_detail(self, db, new_doctor_user, api_client):
        """
        Test doctor detail response status.
        """
        api_client.force_authenticate(new_doctor_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200

    def test_doctor_update(self, db, new_doctor_user, api_client):
        """
        Test doctor update response status.
        """
        api_client.force_authenticate(new_doctor_user)
        assert new_doctor_user.first_name == 'omar'
        response = api_client.patch(self.url, self.data)
        new_doctor_user.refresh_from_db()
        assert response.status_code == 200
        assert new_doctor_user.first_name == 'test name' 


class TestDoctorList:

    url = reverse('doctors-api:doctor-list')

    def test_doctor_list(self, db, new_doctor_user, api_client):
        """
        Test doctor retrieve list response status.
        """
        api_client.force_authenticate(new_doctor_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 1


class DoctorClinicList:

    url = reverse('doctors-api:doctor-clinic-list')

    def test_doctor_clinic_list(self, db, new_doctor_user, new_clinic, api_client):
        """
        Test doctor clinic list response status.
        """
        api_client.force_authenticate(new_doctor_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 1