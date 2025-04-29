from django.contrib import admin
from .models import FieldGroup, FieldDefinition, EmployeeFieldValue

@admin.register(FieldGroup)
class FieldGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(FieldDefinition)
class FieldDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name','group','field_type','required')
    list_filter = ('group','field_type')

@admin.register(EmployeeFieldValue)
class EmployeeFieldValueAdmin(admin.ModelAdmin):
    list_display = ('employee','definition')
