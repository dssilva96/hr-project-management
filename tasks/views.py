from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import TaskForm
from .models import Task


@login_required
def task_list(request):
    tasks = Task.objects.select_related(
        'phase',
        'phase__project',
        'assigned_to',
        'assigned_team',
    ).order_by('due_date', '-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('tasks:list')
    else:
        form = TaskForm()

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
            'form_title': 'Create task',
            'submit_label': 'Create task',
        },
    )


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    next_url = get_safe_next_url(request)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            if next_url:
                return redirect(next_url)
            return redirect('tasks:list')
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
            'task': task,
            'form_title': 'Edit task',
            'submit_label': 'Save changes',
            'next_url': next_url,
        },
    )


def get_safe_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return ''
