from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField("ФИО", max_length=255, blank=True)

    def __str__(self):
        return self.username