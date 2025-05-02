from django.db import models

class FieldGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class FieldDefinition(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('multiline', 'Multiline'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('file', 'File'),
        ('select', 'Select'),
        ('multiselect', 'MultiSelect'),
        ('boolean', 'Boolean'),
        ('email', 'Email'),
        ('url', 'URL'),
        ('phone', 'Phone'),
        ('currency', 'Currency')
    ]
    group = models.ForeignKey(
        FieldGroup, related_name='definitions', on_delete=models.CASCADE
    )
    code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    options = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.group.name} - {self.label}"

class FieldDefinitionValue(models.Model):
    employee = models.ForeignKey(
        'employees.Employee', related_name='dynamic_fields', on_delete=models.CASCADE, null=True, blank=True
    )
    definition = models.ForeignKey(
        FieldDefinition, related_name='values', on_delete=models.CASCADE, null=True, blank=True
    )
    value_text = models.TextField(blank=True, null=True)
    value_number = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    value_date = models.DateField(blank=True, null=True)
    value_file = models.FileField(blank=True, null=True, upload_to='fields/')
    value_select = models.CharField(blank=True, null=True, max_length=200)
    value_list = models.JSONField(blank=True, null=True)  # for multiline/multiselect

    class Meta:
        unique_together = ('employee', 'definition')

    def __str__(self):
        return f"{self.employee} - {self.definition.code}"