from django.urls import path
from .views import UserSettingsRetrieveUpdateAPI

urlpatterns = [
    path('', UserSettingsRetrieveUpdateAPI.as_view(), name='user-settings'),
]
