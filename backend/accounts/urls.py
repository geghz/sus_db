from rest_framework.routers import DefaultRouter
from .views import AdminUserViewSet

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='account-user')

urlpatterns = router.urls
