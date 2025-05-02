from rest_framework import serializers
from django.apps import apps
from .models import Direction, Employee
from tags.serializers import TagSerializer
from tags.models import Tag
from roles.serializers import PositionSerializer

# Получаем модель Position без прямого импорта, чтобы избежать циклических зависимостей
Position = apps.get_model('roles', 'Position')

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer(read_only=True)
    direction_id = serializers.PrimaryKeyRelatedField(
        queryset=Direction.objects.all(), write_only=True, source='direction'
    )
    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), write_only=True, source='position'
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags'
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'birth_date',
            'direction', 'direction_id',
            'position', 'position_id',
            'tags', 'tag_ids',
            'phone_number', 'email'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        employee = Employee.objects.create(**validated_data)
        employee.tags.set(tags)
        return employee

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags is not None:
            instance.tags.set(tags)
        instance.save()
        return instance