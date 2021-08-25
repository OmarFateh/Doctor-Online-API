import json

from django.urls import reverse


class TestUpdateDetailPatient:

    data = {'first_name': 'test name'}
    url = reverse('patients-api:patient-profile-detail-update')

    def test_patient_detail(self, db, new_patient_user, api_client):
        """
        Test patient detail response status.
        """
        api_client.force_authenticate(new_patient_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200

    def test_patient_update(self, db, new_patient_user, api_client):
        """
        Test patient update response status.
        """
        api_client.force_authenticate(new_patient_user)
        assert new_patient_user.first_name == 'omar'
        response = api_client.patch(self.url, self.data)
        new_patient_user.refresh_from_db()
        assert response.status_code == 200
        assert new_patient_user.first_name == 'test name'


class TestPatientClinicReservationList:

    url = reverse('patients-api:patient-reservation-list')

    def test_patient_reservation_list(self, db, new_patient_user, new_reservation, api_client):
        """
        Test patient reservation list response status.
        """
        api_client.force_authenticate(new_patient_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 1