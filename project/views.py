from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from tasks.forms import TaskForm

from .forms import ProjectForm, ProjectPhaseForm
from .models import Project, ProjectPhase


@login_required
def project_list(request):
    projects = Project.objects.select_related('manager').order_by('-created_at')
    status_counts = {
        status: projects.filter(status=status).count()
        for status, _label in Project.STATUS_CHOICES
    }
    return render(
        request,
        'project/project_list.html',
        {
            'projects': projects,
            'status_counts': status_counts,
        },
    )


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('manager').prefetch_related(
            'phases',
            'phases__tasks',
            'phases__tasks__assigned_to',
            'phases__tasks__assigned_team',
        ),
        project_id=project_id,
    )
    timeline_items = build_project_timeline(project)
    phases = project.phases.all()
    tasks = [
        task
        for phase in phases
        for task in phase.tasks.all()
    ]
    return render(
        request,
        'project/project_detail.html',
        {
            'project': project,
            'phases': phases,
            'tasks': tasks,
            'timeline_items': timeline_items,
        },
    )


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            create_default_phase(project)
            messages.success(request, 'Project created successfully.')
            return redirect('project:detail', project_id=project.project_id)
    else:
        form = ProjectForm()

    return render(
        request,
        'project/project_form.html',
        {
            'form': form,
            'form_title': 'Create project',
            'submit_label': 'Create project',
        },
    )


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project:detail', project_id=project.project_id)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'project/project_form.html',
        {
            'form': form,
            'project': project,
            'form_title': 'Edit project',
            'submit_label': 'Save changes',
        },
    )


@login_required
def project_cancel(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)

    if request.method == 'POST':
        project.status = 'cancelled'
        project.save(update_fields=['status', 'updated_at'])
        messages.warning(request, 'Project cancelled.')
        return redirect('project:detail', project_id=project.project_id)

    return render(request, 'project/project_cancel.html', {'project': project})


@login_required
def project_phase_create(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)

    if request.method == 'POST':
        form = ProjectPhaseForm(request.POST)
        if form.is_valid():
            phase = form.save(commit=False)
            phase.project = project
            phase.save()
            messages.success(request, 'Project phase added.')
            return redirect('project:detail', project_id=project.project_id)
    else:
        next_order = project.phases.count() + 1
        form = ProjectPhaseForm(initial={'order': next_order})

    return render(
        request,
        'project/project_phase_form.html',
        {
            'form': form,
            'project': project,
            'form_title': 'Add project phase',
            'submit_label': 'Add phase',
        },
    )


@login_required
def project_task_create(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    create_default_phase(project)

    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added to project.')
            return redirect('project:detail', project_id=project.project_id)
    else:
        form = TaskForm(project=project, initial={'phase': project.phases.first()})

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
            'project': project,
            'form_title': f'Add task to {project.name}',
            'submit_label': 'Add task',
            'back_url': 'project:detail',
        },
    )


def build_project_timeline(project):
    items = [
        {
            'title': 'Project created',
            'date': project.created_at,
            'description': 'The project record was created in the workspace.',
            'icon': 'bi-plus-circle',
        },
        {
            'title': 'Planned start',
            'date': project.start_date,
            'description': project.description or 'Work is scheduled to begin.',
            'icon': 'bi-rocket-takeoff',
        },
    ]

    for phase in project.phases.all():
        items.append(
            {
                'title': phase.name,
                'date': phase.start_date,
                'description': phase.description or 'Project phase milestone.',
                'icon': 'bi-diagram-3',
            }
        )
        if phase.end_date:
            items.append(
                {
                    'title': f'{phase.name} completed',
                    'date': phase.end_date,
                    'description': 'Phase target completion date.',
                    'icon': 'bi-check2-circle',
                }
            )

    items.append(
        {
            'title': 'Target completion',
            'date': project.end_date,
            'description': f'Current project status: {project.get_status_display()}.',
            'icon': 'bi-flag',
        }
    )

    if project.status == 'cancelled':
        items.append(
            {
                'title': 'Project cancelled',
                'date': timezone.localdate(project.updated_at),
                'description': 'The project has been cancelled and is no longer active.',
                'icon': 'bi-x-circle',
            }
        )

    return sorted(items, key=lambda item: timeline_sort_date(item['date']))


def create_default_phase(project):
    if not project.phases.exists():
        ProjectPhase.objects.create(
            project=project,
            name='General',
            description='Default phase for project tasks.',
            order=1,
            start_date=project.start_date,
            end_date=project.end_date,
        )


def timeline_sort_date(value):
    if not value:
        return timezone.localdate()

    if hasattr(value, 'date'):
        return value.date()

    return value



