from rest_framework import serializers
from .models import FieldGroup, FieldDefinition, EmployeeFieldValue

class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = ('id','group','name','field_type','required')

class FieldGroupSerializer(serializers.ModelSerializer):
    definitions = FieldDefinitionSerializer(many=True, read_only=True)

    class Meta:
        model = FieldGroup
        fields = [
            'id',
            'name',
            'code',
            'has_expiry',
            'definitions',
        ]

class EmployeeFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFieldValue
        fields = ('id','employee','definition','value_text','value_date','value_file')
