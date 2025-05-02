from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PositionViewSet, RoleViewSet, PermissionViewSet,
    RolePermissionViewSet, RoleFieldPermissionViewSet, RoleAssignmentViewSet
)

router = DefaultRouter()
router.register(r'positions', PositionViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'role-permissions', RolePermissionViewSet)
router.register(r'role-field-permissions', RoleFieldPermissionViewSet)
router.register(r'role-assignments', RoleAssignmentViewSet)

urlpatterns = router.urls