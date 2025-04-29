from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    full_name = models.CharField("ФИО", max_length=255, blank=True)

    def __str__(self):
        return self.username
    
class UserSettings(models.Model):
     """
     Хранит персональные настройки интерфейса для пользователя.
     """
     user = models.OneToOneField(
         settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE,
         primary_key=True,
         related_name='settings'
     )
     THEME_CHOICES = [
         ('light', 'Светлая'),
         ('dark', 'Тёмная'),
     ]
     theme = models.CharField(
         max_length=10,
         choices=THEME_CHOICES,
         default='light',
         help_text='Цветовая тема интерфейса'
     )
     DENSITY_CHOICES = [
         ('comfortable', 'Комфортная'),
         ('compact', 'Компактная'),
     ]
     density = models.CharField(
         max_length=12,
         choices=DENSITY_CHOICES,
         default='comfortable',
         help_text='Плотность интерфейса'
     )
     tooltips_on = models.BooleanField(
         default=True,
         help_text='Показывать подсказки'
     )
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
         verbose_name = 'Настройка пользователя'
         verbose_name_plural = 'Настройки пользователей'

     def __str__(self):
         return f"Settings for {self.user.username}"
