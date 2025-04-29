from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework import mixins, viewsets, permissions
from .models import UserSettings
from .serializers import (
    AdminUserSerializer,
    UserSettingsSerializer
)

User = get_user_model()

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    CRUD для всех пользователей – доступен только админу.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]


class UserSettingsViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # get_or_create сразу создаёт запись, если её нет
        settings_obj, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return settings_obj