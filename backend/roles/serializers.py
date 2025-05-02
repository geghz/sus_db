from rest_framework import serializers
from .models import (
    Position, Role, Permission,
    RolePermission, RoleFieldPermission, RoleAssignment
)

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'name']

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']

class RoleFieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleFieldPermission
        fields = ['id', 'role', 'field_group', 'can_view', 'can_edit']

class RoleSerializer(serializers.ModelSerializer):
    directions = PositionSerializer(many=True, read_only=True)
    positions = PositionSerializer(many=True, read_only=True)
    role_permissions = RolePermissionSerializer(many=True, read_only=True)
    field_permissions = RoleFieldPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description',
            'directions', 'positions',
            'role_permissions', 'field_permissions'
        ]

class RoleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = ['id', 'user', 'role']