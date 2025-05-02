from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Tag, TagRequest
from .serializers import TagSerializer, TagRequestSerializer

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Tag.objects.filter(is_system=True)
        return Tag.objects.filter(Q(is_system=True) | Q(owner=user))

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def request_system(self, request, pk=None):
        tag = self.get_object()
        if tag.is_system:
            return Response({"detail": "Already a system tag."}, status=400)
        TagRequest.objects.create(user=request.user, tag_name=tag.name)
        return Response({"detail": "Request submitted."}, status=201)

class TagRequestViewSet(viewsets.ModelViewSet):
    queryset = TagRequest.objects.all()
    serializer_class = TagRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        req = self.get_object()
        req.status = TagRequest.APPROVED
        req.save()
        Tag.objects.create(name=req.tag_name, is_system=True)
        req.delete()
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        req = self.get_object()
        req.status = TagRequest.REJECTED
        req.save()
        return Response({"status": "rejected"})
