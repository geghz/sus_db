from rest_framework.routers import DefaultRouter
from .views import FieldGroupViewSet, FieldDefinitionViewSet, EmployeeFieldValueViewSet

router = DefaultRouter()
router.register(r'field-groups', FieldGroupViewSet, basename='fieldgroup')
router.register(r'field-definitions', FieldDefinitionViewSet, basename='fielddefinition')
router.register(r'field-values', EmployeeFieldValueViewSet, basename='fieldvalue')

urlpatterns = router.urls
