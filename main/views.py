from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Q
from main.models import Employee, Attendance
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeeForm, DepartmentForm


@login_required
def home(request):
    employees = Employee.objects.all()
    total_employees = employees.count()
    context = {'employees': employees, 'total_employees': total_employees}
    return render(request, 'main/index.html', context)


@login_required
def all_employees(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request,'main/all_employees.html', context)


@login_required
def add_employee(request):
    form = EmployeeForm()
    if request.user.is_superuser:
        if request.method == 'POST':
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:home')
        else:
            form = EmployeeForm()
    return render(request, 'main/add_employee.html', {'form': form})


@login_required
def add_department(request):
    form = DepartmentForm()
    if request.user.is_superuser:
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:home')
        else:
            form = DepartmentForm()
    return render(request, 'main/add_department.html', {'form': form})


@login_required
def attendance(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            date = request.POST.get('date')
            if Attendance.objects.filter(date=date).exists():
                messages.error(request, f"Attendance for {date} already exists.")
                return redirect('main:attendance')
            else:
                for employee, status in request.POST.items():

                    if employee.startswith('status-'):
                        employee_id = employee[7:]
                        employee = Employee.objects.get(slug=employee_id)
                        new_attendance = Attendance.objects.create(employee=employee, date=date, status=status)
                        new_attendance.save()

                for employee, status in request.POST.items():
                    if employee.startswith('entry-'):
                        employee_id = employee[6:]
                        employee = Employee.objects.get(slug=employee_id)
                        attendance_obj = Attendance.objects.get(employee=employee, date=date)
                        attendance_obj.entry_time = status
                        attendance_obj.save()

                    elif employee.startswith('leave-'):
                        employee_id = employee[6:]
                        employee = Employee.objects.get(slug=employee_id)
                        attendance_obj = Attendance.objects.get(employee=employee, date=date)
                        attendance_obj.leave_time = status
                        attendance_obj.save()

                messages.success(request, f"Attendance for {date} added.")
                return redirect('main:home')
        else:
            employees = Employee.objects.all()
            context = {'employees': employees}
            return render(request, 'main/attendance_table.html', context)
    else:
        return redirect('main:home')


@login_required
def get_attendance_report(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    if request.user.is_superuser:
        if request.method == 'POST':
            start = request.POST.get('start')
            end = request.POST.get('end')
            if request.POST.get('username'):
                username = request.POST.get('username')
                if username == 'All Employees':
                    attendance_list = Attendance.objects.filter(date__range=(start, end))
                    context = {'attendance_list': attendance_list, 'employees': employees}
                    return render(request, 'main/attendance_report.html', context)
                else:
                    employee = Employee.objects.get(slug=username)
                    attendance_list = Attendance.objects.filter(employee=employee, date__range=(start, end))
                    context = {'attendance_list': attendance_list, 'employees': employees}
                    return render(request, 'main/attendance_report.html', context)
    return render(request, 'main/attendance_report.html', context)


@login_required
def get_employee_attendance(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    if request.user.is_superuser:
        if request.method == 'POST':
            start = request.POST.get('start')
            end = request.POST.get('end')
            if request.POST.get('username'):
                username = request.POST.get('username')
                if username == 'All Employees':
                    attendance_list = Attendance.objects.filter(date__range=(start, end)).values('employee__employee', 'employee__department__department_name', 'employee__salary_per_day').annotate(present=Count('status', filter=Q(status='Present')), absent=Count('status', filter=Q(status='Absent')))
                    print(attendance_list)
                    emp_sal = []
                    for salary in attendance_list:
                        sal = salary['present'] * salary['employee__salary_per_day']
                        emp_sal.append(salary['employee__salary_per_day'] * salary['present'])
                        salary['employee__salary'] = sal
                    print(emp_sal)
                    context = {'attendance_list': attendance_list, 'start': start, 'end': end, 'employees': employees, 'emp_sal': emp_sal}
                    return render(request, 'main/attendance_combined.html', context)
                else:
                    employee = Employee.objects.get(slug=username)
                    attendance_list = Attendance.objects.filter(employee=employee, date__range=(start, end)).values('employee__employee').annotate(present=Count('status', filter=Q(status='Present')), absent=Count('status', filter=Q(status='Absent')))
                    total_salary = attendance_list.values('present')
                    for salary in total_salary:
                        print(salary['present'] * employee.salary_per_day)
                    context = {'attendance_list': attendance_list, 'start': start, 'end': end, 'employees': employees}
                    return render(request, 'main/attendance_combined.html', context)
    return render(request, 'main/attendance_combined.html', context)


@login_required
def edit_employee(request, uid):
    employee = Employee.objects.get(uid=uid)
    form = EmployeeForm(instance=employee)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                messages.success(request, 'Employee has been updated.')
                return redirect('main:all_employees')
        else:
            form = EmployeeForm(instance=employee)
    return render(request,'main/edit_employee.html', {'form': form, 'employee': employee})
