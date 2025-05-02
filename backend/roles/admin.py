from django.contrib import admin
from .models import (
    Position, Role, Permission,
    RolePermission, RoleFieldPermission, RoleAssignment
)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('directions', 'positions')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')

@admin.register(RoleFieldPermission)
class RoleFieldPermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'field_group', 'can_view', 'can_edit')

@admin.register(RoleAssignment)
class RoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')