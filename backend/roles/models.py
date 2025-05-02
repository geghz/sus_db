from django.db import models
from django.conf import settings
from employees.models import Direction

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField("Роль", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)
    directions = models.ManyToManyField(
        Direction, blank=True, related_name='roles'
    )
    positions = models.ManyToManyField(
        Position, blank=True, related_name='roles'
    )

    def __str__(self):
        return self.name

class Permission(models.Model):
    code = models.CharField("Код", max_length=100, unique=True)
    name = models.CharField("Название", max_length=200)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='role_permissions'
    )
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.code}"

class RoleFieldPermission(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='field_permissions'
    )
    field_group = models.ForeignKey(
        'fields.FieldGroup', on_delete=models.CASCADE
    )
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'field_group')

    def __str__(self):
        return f"{self.role.name} - {self.field_group.name}"

class RoleAssignment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roles'
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} -> {self.role.name}"