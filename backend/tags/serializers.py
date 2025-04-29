from rest_framework import serializers
from .models import Tag, TagRequest

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'system')

class TagRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TagRequest
        fields = ('id', 'user', 'tag_name', 'status', 'created_at')
        read_only_fields = ('status', 'created_at', 'user')
