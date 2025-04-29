from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import UserSettings
from .serializers import UserSettingsSerializer

class UserSettingsRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    """
    GET  /api/user-settings/     ← получить настройки текущего пользователя
    PUT  /api/user-settings/     ← сохранить изменения
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSettingsSerializer

    def get_object(self):
        obj, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return obj
