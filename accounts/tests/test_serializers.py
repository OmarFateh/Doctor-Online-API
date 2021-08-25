from django.urls import reverse

from accounts.models import User
from accounts.serializers import UserSerializer, UserLoginSerializer, PassowordChangeSerializer


class TestUserSerializer:
    
    data = {'first_name': 'test', 'last_name': 'name', 'email': 'testemail@gmail.com', 
            'email2': 'testemail@gmail.com', 'user_type': 'P', 'password': 'admin1600', 
            'password2': 'admin1600'}

    def test_valid_serializer(self, db):
        """
        Test valid user serializer data.
        """
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == True

    def test_emails_mismatch(self, db):
        """
        Test two emails don't match.
        """
        self.data['email2'] = 'testemail2@gmail.com'
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'The two Emails must match.'
        self.data['email2'] = 'testemail@gmail.com'

    def test_passwords_mismatch(self, db):
        """
        Test two password don't match.
        """
        self.data['password2'] = 'admin160'
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['password'][0] == 'The two Passwords must match.'

    def test_password_invalid(self, db):
        """
        Test password is invalid.
        """
        self.data['password'] = 'admin'
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False


class TestLoginSerializer:
    
    data = {'email': 'testemail@gmail.com', 'password': 'admin1600'}

    def test_valid_serializer(self, db):
        """
        Test valid login serializer data.
        """
        User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_active=True)
        serializer = UserLoginSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestPassowordChangeSerializer:
    
    data = {'old_password': 'admin1600', 'new_password1': 'admin160', 'new_password2': 'admin160'}
    url = reverse('users-api:password-change')

    def test_valid_serializer(self, db, api_factory):
        """
        Test valid serializer data.
        """
        # data is valid 
        user = User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_active=True)
        request = api_factory.get(self.url)
        request.user = user
        serializer = PassowordChangeSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == True
        # old password is incorrect
        self.data['old_password'] = 'admin16'
        serializer = PassowordChangeSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == False
        assert serializer.errors['old_password'][0] == 'Password is incorrect.'
        # two passwords don't match
        self.data['old_password'] = 'admin1600'
        self.data['new_password2'] = 'admin16000'
        serializer = PassowordChangeSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == False
        assert serializer.errors['new_password1'][0] == 'The two Passwords must match.'