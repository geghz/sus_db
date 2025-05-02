from django.db import models
from employees.models import Employee
from fields.models import FieldGroup

class Document(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents',
        blank=True,
        null=True
    )
    field_group = models.ForeignKey(
        FieldGroup,
        on_delete=models.CASCADE,
        related_name='documents',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.employee.full_name} — {self.field_group.name}"

class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='versions',
        blank=True,
        null=True
    )
    number = models.CharField("Номер версии", max_length=100, null=True, blank=True)
    expiration_date = models.DateField("Дата истечения", null=True, blank=True)
    file = models.FileField("Скан документа", upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.document.field_group.name} v{self.number or '1'}"