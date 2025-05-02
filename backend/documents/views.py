from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer
from .permissions import DocumentPermission

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, DocumentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'field_group']

class DocumentVersionViewSet(viewsets.ModelViewSet):
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [IsAuthenticated, DocumentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['document', 'expiration_date']