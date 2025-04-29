from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from .serializers import AdminUserSerializer

User = get_user_model()

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    CRUD для всех пользователей – доступен только админу.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
