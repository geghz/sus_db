from django.db import models
from employees.models import Employee

class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    name = models.CharField("Название группы", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.full_name} – {self.name}"

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions', null=True, blank=True)
    number = models.CharField("Номер документа", max_length=100, null=True, blank=True)
    expiration_date = models.DateField("Дата истечения", null=True, blank=True)
    file = models.FileField("Скан", upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.document.name} v{self.number}"

class DocumentType(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    default_expiry_days = models.PositiveIntegerField(
        help_text="Через сколько дней по умолчанию истекает документ этого типа"
    )

    def __str__(self):
        return self.name