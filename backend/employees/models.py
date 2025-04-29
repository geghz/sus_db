from django.db import models
from accounts.models import CustomUser
from tags.models import Tag

class Direction(models.Model):
    name = models.CharField("Направление", max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='employees'
    )
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, related_name='employees')
    position = models.CharField("Должность", max_length=100)
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='managed_employees')
    hired_at = models.DateField("Дата приема", null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.full_name
