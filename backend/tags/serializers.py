from rest_framework import serializers
from .models import Tag, TagRequest

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'is_system', 'owner']

class TagRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRequest
        fields = ['id', 'tag_name', 'status', 'user', 'created_at']
        read_only_fields = ['status', 'user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        tag_name = validated_data['tag_name']
        return TagRequest.objects.create(user=user, tag_name=tag_name)
