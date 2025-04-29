from django.db import models
from django.conf import settings

class DashboardConfig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget_layout = models.JSONField(default=dict)

    class Meta:
        unique_together = ('user',)