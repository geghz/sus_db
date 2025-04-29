from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ('pending', 'В ожидании'),
    ('approved', 'Одобрен'),
    ('rejected', 'Отклонён'),
]

class Tag(models.Model):
    name = models.CharField("Имя тега", max_length=100, unique=True)
    system = models.BooleanField("Системный", default=False)

    def __str__(self):
        return self.name

class TagRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags_tag_requests', related_query_name='tag_request')
    tag_name = models.CharField("Запрошенный тег", max_length=100)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tag_name} ({self.status})"
