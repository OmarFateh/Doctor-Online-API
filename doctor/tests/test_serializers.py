from django.urls import reverse

from accounts.models import User
from doctor.serializers import DoctorCreateSerializer, DoctorDetailSerializer


class TestDoctorCreateSerializer:
    
    data = {'user':{'first_name': 'test', 'last_name': 'name', 'email': 'testemail@gmail.com', 
                'email2': 'testemail@gmail.com', 'password': 'admin1600', 'password2': 'admin1600'
            },
            'info': 'info', 'specialization': 'specialization'
            }

    def test_valid_serializer(self, db):
        """
        Test valid doctor create serializer data.
        """
        serializer = DoctorCreateSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestDoctorDetailSerializer:
    
    data = {'first_name': 'test name', 'email': 'testemail1@gmail.com', 'info': 'info test'}
    url = reverse('doctors-api:doctor-profile-detail-update')

    def test_valid_serializer(self, db, api_factory):
        """
        Test valid doctor detail serializer data.
        """
        # data is valid 
        user = User.objects.create_user(email='testemail1@gmail.com', password='admin1600', user_type='D')
        request = api_factory.get(self.url)
        request.user = user
        serializer = DoctorDetailSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == True