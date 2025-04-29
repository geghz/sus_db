from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import TagRequest, PermissionRequest
from .serializers import TagRequestSerializer, PermissionRequestSerializer

from tags.models import Tag
from roles.models import RoleAssignment
from notifications.models import Notification

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class TagRequestViewSet(viewsets.ModelViewSet):
    """
    GET (Admin)  — все запросы
    GET (User)   — только свои
    POST         — создать новый TagRequest
    PATCH/PUT    — Admin меняет status → автоматически создаёт Tag + Notification
    """
    queryset = TagRequest.objects.all().order_by('-created_at')
    serializer_class = TagRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        old = self.get_object()
        inst = serializer.save()
        if old.status != inst.status:
            if inst.status == TagRequest.APPROVED:
                Tag.objects.create(name=inst.tag_name, system=False)
                Notification.objects.create(
                    user=inst.user,
                    message=f"Your tag request '{inst.tag_name}' has been approved."
                )
            elif inst.status == TagRequest.REJECTED:
                Notification.objects.create(
                    user=inst.user,
                    message=f"Your tag request '{inst.tag_name}' has been rejected."
                )


class PermissionRequestViewSet(viewsets.ModelViewSet):
    """
    GET (Admin)  — все запросы
    GET (User)   — только свои
    POST         — создать новый PermissionRequest
    PATCH/PUT    — Admin меняет status → создаёт RoleAssignment + Notification
    """
    queryset = PermissionRequest.objects.all().order_by('-created_at')
    serializer_class = PermissionRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        old = self.get_object()
        inst = serializer.save()
        if old.status != inst.status:
            if inst.status == PermissionRequest.APPROVED:
                RoleAssignment.objects.create(user=inst.user, role=inst.role)
                Notification.objects.create(
                    user=inst.user,
                    message=f"Your permission request '{inst.role.name}' has been approved."
                )
            elif inst.status == PermissionRequest.REJECTED:
                Notification.objects.create(
                    user=inst.user,
                    message=f"Your permission request '{inst.role.name}' has been rejected."
                )
