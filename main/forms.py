from django import forms
from .models import Employee, Department


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee', 'position', 'department', 'phone_number', 'salary_per_day', 'hire_date', 'address']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']
