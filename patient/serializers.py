from rest_framework import serializers

from accounts.serializers import UserSerializer
from accounts.mixins import UserUpdateMixins
from .models import Patient


class PatientCreateSerializer(serializers.ModelSerializer):
    """
    A serializer to create new patient.
    """
    user = UserSerializer(required=True)
    gender = serializers.ChoiceField(choices=Patient.GENDER_CHOICES, default="M")

    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone', 'gender', 'birthdate']

    def create(self, validated_data):
        """
        Create user obj with user nested serializer.
        Assign data values to user patient and save it.
        """
        user_data = validated_data['user']
        user_obj = UserSerializer.create(UserSerializer(context={"user_type": "P"}), 
                            validated_data=user_data)
        # assign keys & values to user patient.
        for key, value in validated_data.items():
            if key != 'user':
                setattr(user_obj.patient, key, value)
        user_obj.patient.save()
        return validated_data


class PatientDetailSerializer(serializers.ModelSerializer, UserUpdateMixins):
    """
    A serializer to display or update patient's data.
    """
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'birthdate']
        extra_kwargs = {'phone': {'required': False}}

    def update(self, instance, validated_data):
        """
        """
        user_dict = validated_data['user']
        if user_dict:
            user_obj = instance.user
            for key, value in user_dict.items():
                setattr(user_obj, key, value)
            user_obj.save()
            validated_data["user"] = user_obj
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance  