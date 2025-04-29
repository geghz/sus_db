from rest_framework.routers import DefaultRouter
from .views import (RoleViewSet, PermissionViewSet,
                    RolePermissionViewSet, RoleAssignmentViewSet)

router = DefaultRouter()
router.register(r'roles', RoleViewSet,basename='role')
router.register(r'permissions', PermissionViewSet,basename='permission')
router.register(r'role-permissions', RolePermissionViewSet,basename='rolepermission')
router.register(r'role-assignments', RoleAssignmentViewSet,basename='roleassignment')

urlpatterns = router.urls
