from rest_framework.routers import DefaultRouter
from .views import TagViewSet, TagRequestViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'tag-requests', TagRequestViewSet, basename='tagrequest')

urlpatterns = router.urls
