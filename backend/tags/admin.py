from django.contrib import admin
from .models import Tag, TagRequest

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'system')

@admin.register(TagRequest)
class TagRequestAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'user', 'status', 'created_at')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for req in queryset:
            req.status='approved'
            req.save()
            Tag.objects.get_or_create(name=req.tag_name, defaults={'system':True})
    approve_requests.short_description = "Одобрить выбранные запросы"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
    reject_requests.short_description = "Отклонить выбранные запросы"
