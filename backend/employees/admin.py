from django.contrib import admin
from .models import Direction, Employee

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'direction', 'position', 'email')
    list_filter = ('direction', 'position', 'tags')
    search_fields = ('first_name', 'last_name', 'email')