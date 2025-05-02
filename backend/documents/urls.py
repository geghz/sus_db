from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentVersionViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'documents/(?P<document_id>[^/.]+)/versions', DocumentVersionViewSet, basename='document-version')

urlpatterns = [
    path('', include(router.urls)),
]