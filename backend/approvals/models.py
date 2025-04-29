from django.db import models
from django.conf import settings
from django.utils import timezone

from roles.models import Role, RoleAssignment
from notifications.models import Notification

class TagRequest(models.Model):
    PENDING  = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING,  'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approval_tag_requests', related_query_name='approval_tag_request')
    tag_name   = models.CharField(max_length=100)
    # tag_group  = models.ForeignKey('tags.TagGroup', null=True, blank=True, on_delete=models.SET_NULL)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag_name} ({self.status})"


class PermissionRequest(models.Model):
    PENDING  = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING,  'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    user       = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name='permission_requests'
                )
    role       = models.ForeignKey(Role, on_delete=models.CASCADE,
                    help_text="Role to grant upon approval")
    expires_at = models.DateTimeField(
                    null=True, blank=True,
                    help_text="Optional expiry for granted role"
                )
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} → {self.role.name} ({self.status})"
