from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentVersionViewSet, DocumentTypeViewSet 

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'document-versions', DocumentVersionViewSet, basename='documentversion')
router.register(r'document-types', DocumentTypeViewSet, basename='documenttype')

urlpatterns = router.urls
