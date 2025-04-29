from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

class UserSettings(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    DENSITY_CHOICES = [
        ('comfortable', 'Comfortable'),
        ('compact', 'Compact'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    density = models.CharField(max_length=20, choices=DENSITY_CHOICES, default='comfortable')
    tooltips_on = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user}"
