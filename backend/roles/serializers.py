from rest_framework import serializers
from .models import Role, Permission, RolePermission, RoleAssignment

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id','code','name')

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ('id','role','permission')

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(source='permissions__permission', many=True, read_only=True)
    class Meta:
        model = Role
        fields = ('id','name','description','permissions')

class RoleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = ('id','user','role')
