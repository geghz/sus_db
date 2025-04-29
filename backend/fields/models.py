from django.db import models
from employees.models import Employee

FIELD_TYPES = [
    ('text','Текст'),
    ('date','Дата'),
    ('file','Файл'),
]

class FieldGroup(models.Model):
    name = models.CharField("Группа полей", max_length=100)
    code = models.CharField(max_length=100, unique=True, blank=True, null=True)

    @property
    def has_expiry(self) -> bool:
        return self.definitions.filter(field_type='date').exists()

    def __str__(self):
        return self.name

class FieldDefinition(models.Model):
    group = models.ForeignKey(FieldGroup, on_delete=models.CASCADE, related_name='definitions')
    name = models.CharField("Название поля", max_length=100)
    field_type = models.CharField("Тип", max_length=10, choices=FIELD_TYPES)
    required = models.BooleanField("Обязательное", default=False)

    def __str__(self):
        return f"{self.group.name} / {self.name}"

class EmployeeFieldValue(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='field_values')
    definition = models.ForeignKey(FieldDefinition, on_delete=models.CASCADE)
    value_text = models.TextField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
    value_file = models.FileField(upload_to='field_values/', blank=True, null=True)

    class Meta:
        unique_together = ('employee','definition')
