from django.contrib import admin
from .models import FieldGroup, FieldDefinition, FieldDefinitionValue

@admin.register(FieldGroup)
class FieldGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(FieldDefinition)
class FieldDefinitionAdmin(admin.ModelAdmin):
    list_display = ('label', 'group', 'field_type')
    list_filter = ('field_type', 'group')
    search_fields = ('label', 'code')

@admin.register(FieldDefinitionValue)
class FieldDefinitionValueAdmin(admin.ModelAdmin):
    list_display = ('employee', 'definition', 'value_text', 'value_date')
    list_filter = ('definition__field_type',)
    search_fields = ('employee__user__first_name', 'employee__user__last_name')