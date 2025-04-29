from rest_framework.routers import DefaultRouter
from .views import TagRequestViewSet, PermissionRequestViewSet

router = DefaultRouter()
router.register('tag-requests', TagRequestViewSet, basename='tagrequest')
router.register('permission-requests', PermissionRequestViewSet, basename='permissionrequest')

urlpatterns = router.urls
