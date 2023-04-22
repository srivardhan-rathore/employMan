from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Department(BaseModel):
    department_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True, default=uuid.uuid4)

    def __str__(self):
        return self.department_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.department_name)
        super(Department, self).save(*args, **kwargs)


class Employee(BaseModel):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee')
    phone_number = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    hire_date = models.DateField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return str(self.employee)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.employee)
        super(Employee, self).save(*args, **kwargs)


class Attendance(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

    def __str__(self):
        return f"{self.employee} {self.date}"
