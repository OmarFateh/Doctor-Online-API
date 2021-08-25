from rest_framework import serializers

from accounts.serializers import UserSerializer
from accounts.mixins import UserUpdateMixins
from .models import Doctor


class DoctorCreateSerializer(serializers.ModelSerializer):
    """
    A serializer to create new doctor.
    """
    user = UserSerializer(required=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'info']

    def create(self, validated_data):
        """
        Create user obj with user nested serializer.
        Assign data values to user doctor and save it.
        """
        user_data = validated_data['user']
        user_obj = UserSerializer.create(UserSerializer(context={"user_type": "D"}), 
                                validated_data=user_data)
        # assign keys & value to user doctor.
        for key, value in validated_data.items():
            if key != 'user':
                setattr(user_obj.doctor, key, value) 
        user_obj.doctor.save()
        return validated_data


class DoctorDetailSerializer(serializers.ModelSerializer, UserUpdateMixins):
    """
    A serializer to display or update doctor's data.
    """
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'specialization', 'info']
        extra_kwargs = {'specialization': {'required': False}, 'info': {'required': False}}

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