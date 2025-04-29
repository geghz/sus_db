from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserSettings

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            # если нужно – группы и права:
            'groups',
            'user_permissions',
        ]
        read_only_fields = ['id']


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Retrieve/Update персональных настроек интерфейса пользователя.
    """
    class Meta:
        model = UserSettings
        fields = ['theme', 'density', 'tooltips_on']