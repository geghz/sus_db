from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from employees.models import Employee
from documents.models import DocumentVersion
from tags.models import TagRequest
from approvals.models import PermissionRequest
from notifications.models import Notification

class DashboardView(APIView):
    """
    Возвращает набор метрик для дашборда:
    - total_employees: всего сотрудников в зоне видимости
    - expiring_documents: сколько документов истекает в ближайшие 30 дней
    - pending_tag_requests: сколько запросов на новые теги ждут одобрения
    - pending_permission_requests: сколько запросов на права ждут одобрения
    - unread_notifications: сколько у текущего пользователя непрочитанных уведомлений
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_superuser:
            total_employees = Employee.objects.count()
        else:
            total_employees = Employee.objects.filter(manager=user).count()

        threshold_date = timezone.now().date() + timedelta(days=30)
        expiring_documents = DocumentVersion.objects.filter(expiry_date__lte=threshold_date).count()

        pending_tag_requests = TagRequest.objects.filter(status='pending').count()

        pending_permission_requests = PermissionRequest.objects.filter(status='pending').count()

        unread_notifications = Notification.objects.filter(
            user=user,
            read=False
        ).count()

        return Response({
            'total_employees': total_employees,
            'expiring_documents': expiring_documents,
            'pending_tag_requests': pending_tag_requests,
            'pending_permission_requests': pending_permission_requests,
            'unread_notifications': unread_notifications,
        })
