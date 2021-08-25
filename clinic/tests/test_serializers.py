from clinic.serializers import ClinicSerializer


class TestClinicSerializer:
    
    data = {'name': 'name', 'price': '500', 'date': '2021-8-5', 'start_time': '7:00', 'end_time': '8:00'}
    
    def test_valid_serializer(self, db):
        """
        Test valid clinic serializer data.
        """
        serializer = ClinicSerializer(data=self.data)
        assert serializer.is_valid() == True

    def test_invalid_start_time(self, db):
        """
        Test invalid start time which is greater than end time.
        """
        self.data['start_time'] = '9:00'
        serializer = ClinicSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['start_time'][0] == 'Start time should be earlier than end time.'  