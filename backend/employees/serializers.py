from rest_framework import serializers
from .models import Direction, Employee

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'name')

class EmployeeSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer(read_only=True)
    direction_id = serializers.PrimaryKeyRelatedField(
        queryset=Direction.objects.all(), write_only=True, source='direction'
    )

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'full_name',
                  'direction', 'direction_id', 'position', 'manager', 'hired_at')
