from django.contrib import admin
from .models import Direction, Employee

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'direction', 'position', 'manager')
    list_filter = ('direction',)
