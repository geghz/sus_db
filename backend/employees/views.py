from rest_framework import viewsets, permissions, filters
from .models import Direction, Employee
from .serializers import DirectionSerializer, EmployeeSerializer
from .filters import EmployeeFilter
from .filters import DynamicFieldOrderingFilter

from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend



class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [permissions.IsAdminUser]

class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]  # + ваши кастомные permission-классы

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        DynamicFieldOrderingFilter
    ]
    filterset_class = EmployeeFilter

    # Поиск по ФИО и email
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
    ]

    # Сортировка по фамилии, направлению и менеджеру
    ordering_fields = [
        'user__last_name',
        'direction__name',
        'manager__last_name',
    ]
    ordering = ['user__last_name']
