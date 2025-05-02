from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from roles.models import Role

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login = attrs.get(self.username_field)
        password = attrs.get("password")
        try:
            user = User.objects.get(Q(username__iexact=login) | Q(email__iexact=login))
            if not user.is_active:
                raise serializers.ValidationError("Пользователь деактивирован.")
            attrs[self.username_field] = user.username
        except User.DoesNotExist:
            pass
        data = super().validate(attrs)
        data.update({"user_id": self.user.id, "username": self.user.username, "email": self.user.email})
        return data

class RoleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    roles = RoleMiniSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'roles']