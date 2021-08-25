from rest_framework import serializers

from doctor.serializers import DoctorDetailSerializer
from patient.serializers import PatientDetailSerializer
from .models import Clinic, Reservation
from .mixins import TimestampMixin


class ClinicSerializer(serializers.ModelSerializer):
    """
    Clinic model serializer.
    """
    is_outdated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Clinic
        fields = ['id', 'uuid', 'name', 'price', 'date', 'start_time', 'end_time', 'is_outdated']
        read_only_fields = ['uuid']

    def get_is_outdated(self, obj):
        return obj.is_outdated

    def validate(self, data):
        """
        Validate that end time is greater than start time.
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if not start_time:
            start_time = self.instance.start_time    
        if not end_time:
            end_time = self.instance.end_time
        if end_time < start_time:
            raise serializers.ValidationError({"start_time":"Start time should be earlier than end time."})
        return data     


class ClinicListSerializer(serializers.ModelSerializer):
    """
    Clinic list model serializer.
    """
    doctor = DoctorDetailSerializer(read_only=True)
    is_outdated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Clinic
        fields = ['id', 'uuid', 'doctor', 'name', 'price', 'date', 'start_time', 'end_time', 'is_outdated']
        read_only_fields = ['uuid']

    def get_is_outdated(self, obj):
        return obj.is_outdated


class ClinicReservationSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Clinic Reservation model serializer with Patient as a nested serializer.
    """
    patient = PatientDetailSerializer(read_only=True)

    class Meta:
        model  = Reservation
        fields = ['id', 'patient', 'is_active', 'created_at', 'updated_at']


class PatientReservationSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Clinic Reservation model serializer with clinic as a nested serializer.
    """
    clinic = ClinicSerializer(read_only=True)

    class Meta:
        model  = Reservation
        fields = ['id', 'clinic', 'is_active', 'created_at', 'updated_at']