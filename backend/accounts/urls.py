from rest_framework.routers import DefaultRouter
from .views import AdminUserViewSet, UserSettingsViewSet

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-user')
router.register(r'user-settings', UserSettingsViewSet, basename='user-settings')

urlpatterns = router.urls