from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Position, Role, Permission,
    RolePermission, RoleFieldPermission, RoleAssignment
)
from .serializers import (
    PositionSerializer, RoleSerializer, PermissionSerializer,
    RolePermissionSerializer, RoleFieldPermissionSerializer, RoleAssignmentSerializer
)

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['directions', 'positions']

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleFieldPermissionViewSet(viewsets.ModelViewSet):
    queryset = RoleFieldPermission.objects.all()
    serializer_class = RoleFieldPermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleAssignmentViewSet(viewsets.ModelViewSet):
    queryset = RoleAssignment.objects.all()
    serializer_class = RoleAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]