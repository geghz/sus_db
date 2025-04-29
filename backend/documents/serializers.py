from rest_framework import serializers
from .models import Document, DocumentVersion, DocumentType

class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ('id', 'number', 'expiration_date', 'file', 'uploaded_at')

class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'employee', 'name', 'versions')

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'code', 'name', 'default_expiry_days']