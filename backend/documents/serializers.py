from rest_framework import serializers
from .models import Document, DocumentVersion

class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ['id', 'document', 'number', 'expiration_date', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'employee', 'field_group', 'versions']

    def create(self, validated_data):
        return Document.objects.create(**validated_data)