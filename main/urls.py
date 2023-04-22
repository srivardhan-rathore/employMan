from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('attendance/', views.attendance, name='attendance'),
    path('report/', views.get_attendance_report, name='report'),
    path('combined_report/', views.get_employee_attendance, name="combined_report"),
    path('all_employees/', views.all_employees, name='all_employees'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('add_department/', views.add_department, name='add_department'),
]
