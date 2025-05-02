from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField("Имя тега", max_length=100, unique=True)
    is_system = models.BooleanField("Системный", default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True,
        related_name="user_tags"
    )

    def __str__(self):
        return self.name

class TagRequest(models.Model):
    PENDING  = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING,  'В ожидании'),
        (APPROVED, 'Одобрен'),
        (REJECTED, 'Отклонён'),
    ]

    user      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags_tag_requests'
    )
    tag_name  = models.CharField("Запрошенный тег", max_length=100)
    status    = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tag_name} ({self.status})"
