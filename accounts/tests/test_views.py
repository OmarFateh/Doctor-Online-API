from django.urls import reverse
from django.shortcuts import get_object_or_404

import pytest

from accounts.models import User
from doctor.models import Doctor
from patient.models import Patient


user_data = {'user':{'first_name': 'test', 'last_name': 'name', 'email': 'testemail@gmail.com', 
                'email2': 'testemail@gmail.com', 'password': 'admin1600', 'password2': 'admin1600'
            },}

class TestRegisterDoctor:

    user_data['info'] = 'info'
    user_data['specialization'] = 'specialization'
    data = user_data
    url = reverse('users-api:register-doctor')

    def test_register_doctor_user(self, db, api_client):
        """
        Test register doctor user response status.
        """
        response = api_client.post(self.url, data=self.data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(user_type='D').count() == 1
        assert Doctor.objects.count() == 1
        assert Doctor.objects.first().user.email == self.data['user']['email']


class TestRegisterPatient:

    user_data['gender'] = 'M'
    user_data['phone'] = '+999999999'
    user_data['birthdate'] = '2021-10-5'
    data = user_data
    url = reverse('users-api:register-patient')

    def test_register_patient_user(self, db, api_client):
        """
        Test register patient user response status.
        """
        response = api_client.post(self.url, data=self.data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(user_type='P').count() == 1
        assert Patient.objects.count() == 1
        assert Patient.objects.first().user.email == self.data['user']['email']
   
 
@pytest.mark.parametrize(
    "email, password, status_code", 
    [
        ('testemail@gmail.com', 'admin1600', 200),
        ('user@example.com', 'invalid_pass', 401),
    ]
)
def test_login(email, password, status_code, api_client, db):
    """
    Test login user response status.
    """
    User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_active=True)
    url = reverse('users-api:login')
    data = {'email': email, 'password': password}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "old_password, new_password1, new_password2, status_code", 
    [
        ('admin1600', 'admin160', 'admin160', 200),
        ('admin1600', 'admin160', 'admin1600', 400),
        ('admin160', 'admin16', 'admin16', 400),
    ]
)
def test_change_password(old_password, new_password1, new_password2, status_code, api_client, db):
    """
    Test password change response status.
    """
    user = User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_active=True)
    api_client.force_authenticate(user)
    url = reverse('users-api:password-change')
    data = {'old_password': old_password, 'new_password1':new_password1, 'new_password2': new_password2}
    response = api_client.put(url, data=data)
    assert response.status_code == status_code