from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from employees.models import Employee
from fields.models import FieldDefinitionValue
from documents.models import DocumentVersion
from approvals.models import TagRequest, PermissionRequest
from datetime import date, timedelta

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Employee.objects.all()

        # Фильтрация по зонам видимости (directions, positions)
        dir_ids = set(user.roles.values_list('directions__id', flat=True))
        pos_ids = set(user.roles.values_list('positions__id', flat=True))
        if dir_ids:
            qs = qs.filter(direction_id__in=dir_ids)
        if pos_ids:
            qs = qs.filter(position_id__in=pos_ids)

        total_employees = qs.count()

        today = date.today()
        in_7_days = today + timedelta(days=7)
        in_30_days = today + timedelta(days=30)

        # Истекающие документы
        expiring_docs_7 = DocumentVersion.objects.filter(expiration_date__range=[today, in_7_days]).count()
        expiring_docs_30 = DocumentVersion.objects.filter(expiration_date__range=[today, in_30_days]).count()

        # Истекающие динамические поля (тип date)
        expiring_fields_7 = FieldDefinitionValue.objects.filter(
            definition__field_type='date',
            value_date__range=[today, in_7_days]
        ).count()
        expiring_fields_30 = FieldDefinitionValue.objects.filter(
            definition__field_type='date',
            value_date__range=[today, in_30_days]
        ).count()

        # Pending-запросы (если admin)
        pending_tag_requests = TagRequest.objects.filter(status='pending').count() if user.is_staff else 0
        pending_perm_requests = PermissionRequest.objects.filter(status='pending').count() if user.is_staff else 0

        return Response({
            'total_employees': total_employees,
            'expiring_documents_7d': expiring_docs_7,
            'expiring_documents_30d': expiring_docs_30,
            'expiring_fields_7d': expiring_fields_7,
            'expiring_fields_30d': expiring_fields_30,
            'pending_tag_requests': pending_tag_requests,
            'pending_permission_requests': pending_perm_requests
        })