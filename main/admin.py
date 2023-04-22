from django.contrib import admin

from .models import Department, Employee, Attendance


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'department_name',
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('slug',)
    date_hierarchy = 'created_at'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'department',
        'phone_number',
        'hire_date',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'employee',
        'department',
        'hire_date',
    )
    search_fields = ('slug',)
    date_hierarchy = 'created_at'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'date',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at', 'employee', 'date')
    date_hierarchy = 'created_at'
