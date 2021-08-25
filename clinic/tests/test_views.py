import json

from django.urls import reverse

from clinic.models import Clinic, Reservation


class TestClinic:

    data = {'name': 'name', 'price': '500', 'date': '2021-8-5', 'start_time': '7:00', 'end_time': '8:00'}
    list_endpoint = reverse('clinics-api:clinic-list')
    create_endpoint = reverse('clinics-api:create-clinic')
    detail_endpoint = reverse('clinics-api:detail-update-delete-clinic',
                        kwargs={"clinic_uuid": '36e6abc3-6c46-4624-8e29-52340ceaf53b'})

    def test_clinic_list(self, db, new_patient_user, new_clinic, api_client):
        """
        Test clinic retrieve list response status.
        """
        api_client.force_authenticate(new_patient_user)
        response = api_client.get(self.list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 1   

    def test_clinic_create(self, db, new_doctor_user, api_client):
        """
        Test clinic create response status.
        """
        api_client.force_authenticate(new_doctor_user)
        assert Clinic.objects.count() == 0
        response = api_client.post(self.create_endpoint, self.data)
        assert response.status_code == 201
        assert Clinic.objects.count() == 1

    def test_clinic_detail(self, db, new_patient_user, new_clinic, api_client):
        """
        Test clinic detail response status.
        """
        api_client.force_authenticate(new_patient_user)
        response = api_client.get(self.detail_endpoint, format='json')
        assert response.status_code == 200

    def test_clinic_update(self, db, new_doctor_user, new_clinic, api_client):
        """
        Test clinic update response status.
        """
        api_client.force_authenticate(new_doctor_user)
        assert new_clinic.name == 'name'
        data = {'name': 'test name'}
        response = api_client.patch(self.detail_endpoint, data)
        new_clinic.refresh_from_db()
        assert response.status_code == 200
        assert new_clinic.name == 'test name'

    def test_clinic_delete(self, db, new_doctor_user, new_clinic, api_client):
        """
        Test clinic delete response status.
        """
        api_client.force_authenticate(new_doctor_user)
        assert Clinic.objects.count() == 1
        response = api_client.delete(self.detail_endpoint)
        assert response.status_code == 204
        assert Clinic.objects.count() == 0 


class TestReservation:

    list_endpoint = reverse('clinics-api:clinic-reservation-list',
                        kwargs={"clinic_uuid": '36e6abc3-6c46-4624-8e29-52340ceaf53b'})
    add_cancel_endpoint = reverse('clinics-api:clinic-add-cancel-reservation',
                        kwargs={"clinic_uuid": '36e6abc3-6c46-4624-8e29-52340ceaf53b'})                        

    def test_reservation_list(self, db, new_doctor_user, new_clinic, new_reservation, api_client):
        """
        Test reservation list response status.
        """
        api_client.force_authenticate(new_doctor_user)
        response = api_client.get(self.list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 1 

    def test_reservation_add_cancel(self, db, new_patient_user, new_patient, new_clinic, api_client):
        """
        Test reservation add/cancel response status.
        """
        api_client.force_authenticate(new_patient_user)
        assert Reservation.objects.count() == 0
        # add reservation
        response = api_client.post(self.add_cancel_endpoint)
        reservation_qs = Reservation.objects.filter(clinic=new_clinic, patient=new_patient)
        assert response.status_code == 200
        assert Reservation.objects.count() == 1
        assert reservation_qs.count() == 1
        assert reservation_qs.first().is_active == True
        # cancel reservation & set it to be inactive
        response = api_client.post(self.add_cancel_endpoint)
        assert response.status_code == 200
        assert reservation_qs.first().is_active == False