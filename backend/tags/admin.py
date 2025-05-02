from django.contrib import admin
from .models import Tag, TagRequest

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_system', 'owner']
    list_filter = ['is_system', 'owner']
    search_fields = ['name']

@admin.register(TagRequest)
class TagRequestAdmin(admin.ModelAdmin):
    list_display = ['tag_name', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tag_name', 'user__username']
