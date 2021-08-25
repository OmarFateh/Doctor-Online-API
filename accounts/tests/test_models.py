import pytest

from accounts.models import User


class TestModel:

    def test_create_user(self, db):
        """
        Test model manager create user method with valid data.
        """
        user = User.objects.create_user(email='normal@user.com', password='admin1600')
        assert user.email == 'normal@user.com'
        assert user.is_staff == False
        assert user.is_superuser == False
        assert user.is_active == True

    def test_empty_password(self, db):
        """
        Test create user method with empty password.
        """
        with pytest.raises(ValueError) as e:
            user1 = User.objects.create_user(email='admin3@gmail.com', password='')
        assert str(e.value) == 'Users must have a password'

    def test_invalid_password(self, db):
        """
        Test create user method with invalid password.
        """
        with pytest.raises(ValueError) as e:
            user2 = User.objects.create_user(email='admin3@gmail.com', password='admin')   
    
    def test_empty_email(self, db):
        """
        Test create user method with empty email.
        """
        with pytest.raises(ValueError) as e:
            user3 = User.objects.create_user(email='', password='admin1600')
        assert str(e.value) == 'Users must have an email address'
    
    def test_not_given_email(self, db):
        """
        Test create user method with not given email.
        """
        with pytest.raises(TypeError) as e:
            user4 = User.objects.create_user(password='admin1600')

    def test_invalid_email(self, db):
        """
        Test create user method with invalid email.
        """
        with pytest.raises(ValueError) as e:
            user5 = User.objects.create_user(email='ahmed', password='admin1600')
        assert str(e.value) == 'You must provide a valid email address.'

    def test_create_superuser(self, db):
        """
        Test model manager create superuser method.
        """
        moderator_user = User.objects.create_superuser(email='admin2@gmail.com', password='admin1600')
        assert User.objects.filter(is_superuser=True).count() == 1
        assert moderator_user.is_staff == True
        assert moderator_user.is_superuser == True
        assert moderator_user.is_active == True
        assert moderator_user.user_type == "M"

    def test_user_str(self, new_patient_user):
        """
        Test user obj str method.
        """
        assert new_patient_user.__str__() == 'testemail@gmail.com'

    def test_user_get_full_name(self, new_patient_user):
        """
        Test user obj get full name method.
        """
        assert new_patient_user.get_full_name() == 'omar fateh'

    def test_user_is_patient(self, new_patient_user):
        """
        Test user obj is patient method.
        """ 
        assert new_patient_user.is_patient() == True       