from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('attendance/', views.attendance, name='attendance'),
    path('report/', views.get_attendance_report, name='report'),
    path('combined_report/', views.get_employee_attendance, name="combined_report"),
]
