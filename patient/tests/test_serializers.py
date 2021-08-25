from django.urls import reverse

from accounts.models import User
from patient.serializers import PatientCreateSerializer, PatientDetailSerializer


class TestPatientCreateSerializer:
    
    data = {'user':{'first_name': 'test', 'last_name': 'name', 'email': 'testemail@gmail.com', 
                'email2': 'testemail@gmail.com', 'password': 'admin1600', 'password2': 'admin1600'
            },
            'gender': 'M', 'phone': '+999999999', 'birthdate': '2021-10-11'
            }

    def test_valid_serializer(self, db):
        """
        Test valid patient create serializer data.
        """
        serializer = PatientCreateSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestPatientDetailSerializer:
    
    data = {'first_name': 'test name', 'email': 'testemail@gmail.com', 'phone': '+520545520'}
    url = reverse('patients-api:patient-profile-detail-update')

    def test_valid_serializer(self, db, api_factory):
        """
        Test valid patient detail serializer data.
        """
        # data is valid 
        user = User.objects.create_user(email='testemail@gmail.com', password='admin1600', user_type='P')
        request = api_factory.get(self.url)
        request.user = user
        serializer = PatientDetailSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == True
        # email already exists
        self.data['email'] = 'testemail2@gmail.com'
        user1 = User.objects.create_user(email='testemail2@gmail.com', password='admin1600', user_type='P')
        serializer = PatientDetailSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'An account with this Email already exists.'