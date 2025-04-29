from django.contrib import admin
from .models import Role, Permission, RolePermission, RoleAssignment

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name','description')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code','name')

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role','permission')

@admin.register(RoleAssignment)
class RoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user','role')
