from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tag, TagRequest
from .serializers import TagSerializer, TagRequestSerializer
from django.db.models import Q

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # системные + одобренные у этого пользователя
        return Tag.objects.filter(
            Q(system=True) |
            Q(tagrequest__user=user, tagrequest__status='approved')
        ).distinct()

class TagRequestViewSet(viewsets.ModelViewSet):
    queryset = TagRequest.objects.all()
    serializer_class = TagRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        req = self.get_object()
        req.status = 'approved'
        Tag.objects.get_or_create(name=req.tag_name, defaults={'system': True})
        req.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        req = self.get_object()
        req.status = 'rejected'
        req.save()
        return Response({'status': 'rejected'})
