
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('authentication.urls')),
    path('api/accounts/', include('accounts.urls')),

    path('api/accounts/', include('accounts.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/fields/', include('fields.urls')),
    path('api/roles/', include('roles.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/requests/', include('approvals.urls')),
    
]
