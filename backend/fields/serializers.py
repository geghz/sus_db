from rest_framework import serializers
from .models import FieldGroup, FieldDefinition, FieldDefinitionValue

class FieldGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldGroup
        fields = ['id', 'name']

class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = ['id', 'group', 'code', 'label', 'field_type', 'options']

class FieldDefinitionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinitionValue
        fields = [
            'id', 'employee', 'definition',
            'value_text', 'value_number', 'value_date',
            'value_file', 'value_select', 'value_list'
        ]