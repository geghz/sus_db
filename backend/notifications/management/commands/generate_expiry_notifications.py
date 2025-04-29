from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from documents.models import DocumentVersion
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Создаёт ежедневные уведомления для руководителей о близком истечении документов.'

    def handle(self, *args, **options):
        days = getattr(settings, 'EXPIRE_NOTIFICATION_DAYS', 7)
        today = timezone.now().date()
        threshold = today + timedelta(days=days)

        # Берём все версии документов, которые истекают между сегодня и threshold
        expiring_versions = DocumentVersion.objects.filter(
            expiry_date__range=(today, threshold)
        ).select_related('document__employee__manager')

        # Собираем по каждому менеджеру число таких документов
        counts = {}
        for version in expiring_versions:
            emp = version.document.employee
            mgr = getattr(emp, 'manager', None)
            if mgr:
                counts[mgr] = counts.get(mgr, 0) + 1

        # Генерируем уведомление для каждого менеджера
        for mgr, cnt in counts.items():
            # формируем сообщение
            msg = (
                f"У {cnt} ваших сотрудников сроки документов истекают "
                f"в течение {days} дней."
            )
            # чтобы не дублировать, проверяем, не было ли такого сегодня
            exists = Notification.objects.filter(
                user=mgr,
                message=msg,
                created_at__date=today
            ).exists()
            if not exists:
                Notification.objects.create(
                    user=mgr,
                    message=msg
                )
                self.stdout.write(f"→ Notification for {mgr}: {msg}")
            else:
                self.stdout.write(f"— Уже есть уведомление для {mgr} сегодня.")
