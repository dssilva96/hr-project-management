from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm, TeamForm
from .models import Employee, Team


@login_required
def employee_list(request):
    employees = Employee.objects.select_related('user').order_by('first_name', 'last_name')
    teams = Team.objects.prefetch_related('members').select_related('lead')

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': employees,
            'teams': teams,
            'active_count': employees.filter(status='active').count(),
            'team_count': teams.count(),
        },
    )


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('employees:list')
    else:
        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'form_title': 'Create employee',
            'submit_label': 'Create employee',
        },
    )


@login_required
def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employees:list')
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'employee': employee,
            'form_title': 'Edit employee',
            'submit_label': 'Save changes',
        },
    )


@login_required
def employee_deactivate(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        employee.status = 'inactive'
        employee.save(update_fields=['status'])
        messages.warning(request, 'Employee marked inactive.')
        return redirect('employees:list')

    return render(request, 'employees/employee_deactivate.html', {'employee': employee})


@login_required
def team_list(request):
    teams = Team.objects.select_related('lead').prefetch_related('members')
    return render(request, 'employees/team_list.html', {'teams': teams})


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related('lead').prefetch_related('members', 'tasks__phase__project'),
        team_id=team_id,
    )
    tasks = team.tasks.select_related('phase', 'phase__project').order_by('due_date', 'priority')
    return render(request, 'employees/team_detail.html', {'team': team, 'tasks': tasks})


@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            messages.success(request, 'Team created successfully.')
            return redirect('employees:team_detail', team_id=team.team_id)
    else:
        form = TeamForm()

    return render(
        request,
        'employees/team_form.html',
        {
            'form': form,
            'form_title': 'Create team',
            'submit_label': 'Create team',
        },
    )


@login_required
def team_edit(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully.')
            return redirect('employees:team_detail', team_id=team.team_id)
    else:
        form = TeamForm(instance=team)

    return render(
        request,
        'employees/team_form.html',
        {
            'form': form,
            'team': team,
            'form_title': 'Edit team',
            'submit_label': 'Save changes',
        },
    )
