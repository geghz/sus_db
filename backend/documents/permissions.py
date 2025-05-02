from rest_framework import permissions
from roles.models import RoleFieldPermission

class DocumentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        user_roles = request.user.roles.all()
        for role in user_roles:
            perm = role.field_permissions.filter(field_group=obj.field_group).first()
            if not perm:
                continue
            if view.action in ['retrieve', 'list'] and perm.can_view:
                return True
            if view.action in ['create', 'update', 'partial_update', 'destroy'] and perm.can_edit:
                return True
        return False