import sys
from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'Уведомления'

    def ready(self):
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM django_apscheduler_djangojob LIMIT 1;"
                )
        except OperationalError:
            return

        from .scheduler import start as start_scheduler
        start_scheduler()
