from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DirectionViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'directions', DirectionViewSet, basename='direction')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]