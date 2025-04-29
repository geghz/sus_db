import logging
from datetime import timedelta
from django.conf import settings
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

from documents.models import DocumentVersion
from notifications.models import Notification

logger = logging.getLogger(__name__)

def generate_expiry_notifications():
    days = getattr(settings, 'EXPIRE_NOTIFICATION_DAYS', 7)
    today = timezone.now().date()
    threshold = today + timedelta(days=days)

    expiring = (
        DocumentVersion.objects
        .filter(expiry_date__range=(today, threshold))
        .select_related('document__employee__manager')
    )
    counts = {}
    for v in expiring:
        mgr = getattr(v.document.employee, 'manager', None)
        if mgr:
            counts[mgr] = counts.get(mgr, 0) + 1

    for mgr, cnt in counts.items():
        msg = (
            f"У {cnt} ваших сотрудников сроки документов истекают "
            f"в течение {days} дней."
        )
        already = Notification.objects.filter(
            user=mgr,
            message=msg,
            created_at__date=today
        ).exists()
        if not already:
            Notification.objects.create(user=mgr, message=msg)
            logger.info(f"Создано уведомление для {mgr}: {msg}")
        else:
            logger.debug(f"Уведомление для {mgr} уже было сегодня.")

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "cron", hour="8", minute="0", id="expiry_notifications")
def scheduled_job():
    generate_expiry_notifications()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Регистрируем задачу, заменяя старую, если она уже есть
    scheduler.add_job(
        func=generate_expiry_notifications,
        trigger="cron",
        hour=8,
        minute=0,
        id="expiry_notifications",
        replace_existing=True,     # <- вот это
        name="Generate daily expiry notifications",
    )

    scheduler.start()
