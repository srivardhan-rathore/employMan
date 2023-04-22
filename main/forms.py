from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee', 'position', 'department', 'phone_number', 'salary', 'hire_date', 'address']
