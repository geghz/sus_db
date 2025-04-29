from rest_framework import serializers
from .models import TagRequest, PermissionRequest

class TagRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRequest
        fields = ['id', 'user', 'tag_name', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']


class PermissionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        fields = ['id', 'user', 'role', 'expires_at', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
