from django.db import models
from django.contrib.auth import get_user_model
from tags.models import Tag
# from roles.models import Position  # removed to avoid circular import

User = get_user_model()

class Direction(models.Model):
    name = models.CharField("Направление", max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='employee_profile'
    )
    first_name = models.CharField("Имя", max_length=100, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=100, null=True, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    direction = models.ForeignKey(
        Direction,
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees'
    )
    position = models.ForeignKey(
        'roles.Position',
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='employees'
    )
    phone_number = models.CharField(
        "Номер телефона",
        max_length=20,
        blank=True
    )
    email = models.EmailField("Email", unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"