from rest_framework import viewsets, permissions
from .models import Document, DocumentVersion, DocumentType
from .serializers import DocumentSerializer, DocumentVersionSerializer, DocumentTypeSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentVersionViewSet(viewsets.ModelViewSet):
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentTypeViewSet(viewsets.ModelViewSet):

    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAdminUser]  # доступ только администратору