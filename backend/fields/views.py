from rest_framework import viewsets, permissions
from .models import FieldGroup, FieldDefinition, EmployeeFieldValue
from .serializers import FieldGroupSerializer, FieldDefinitionSerializer, EmployeeFieldValueSerializer

class FieldGroupViewSet(viewsets.ModelViewSet):
    queryset = FieldGroup.objects.all()
    serializer_class = FieldGroupSerializer
    permission_classes = [permissions.IsAdminUser]

class FieldDefinitionViewSet(viewsets.ModelViewSet):
    queryset = FieldDefinition.objects.all()
    serializer_class = FieldDefinitionSerializer
    permission_classes = [permissions.IsAdminUser]

class EmployeeFieldValueViewSet(viewsets.ModelViewSet):
    queryset = EmployeeFieldValue.objects.all()
    serializer_class = EmployeeFieldValueSerializer
    permission_classes = [permissions.IsAuthenticated]
