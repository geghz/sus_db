from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FieldGroupViewSet,
    FieldDefinitionViewSet,
    FieldDefinitionValueViewSet
)

router = DefaultRouter()
router.register(r'field-groups', FieldGroupViewSet, basename='fieldgroup')
router.register(r'field-defs', FieldDefinitionViewSet, basename='fielddefinition')
router.register(r'field-values', FieldDefinitionValueViewSet, basename='fieldvalue')

urlpatterns = [
    path('', include(router.urls)),
]