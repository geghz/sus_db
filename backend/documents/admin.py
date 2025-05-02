from django.contrib import admin
from .models import Document, DocumentVersion

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'field_group')
    list_filter = ('field_group', 'employee')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'number', 'expiration_date', 'uploaded_at')
    list_filter = ('expiration_date',)
    date_hierarchy = 'uploaded_at'