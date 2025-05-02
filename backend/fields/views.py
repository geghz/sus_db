from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import FieldGroup, FieldDefinition, FieldDefinitionValue
from .serializers import (
    FieldGroupSerializer,
    FieldDefinitionSerializer,
    FieldDefinitionValueSerializer
)

class FieldGroupViewSet(viewsets.ModelViewSet):
    queryset = FieldGroup.objects.all()
    serializer_class = FieldGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class FieldDefinitionViewSet(viewsets.ModelViewSet):
    queryset = FieldDefinition.objects.all()
    serializer_class = FieldDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'field_type']

class FieldDefinitionValueViewSet(viewsets.ModelViewSet):
    queryset = FieldDefinitionValue.objects.all()
    serializer_class = FieldDefinitionValueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'definition']