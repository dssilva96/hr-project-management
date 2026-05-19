from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('new/', views.project_create, name='create'),
    path('<uuid:project_id>/', views.project_detail, name='detail'),
    path('<uuid:project_id>/phases/new/', views.project_phase_create, name='phase_create'),
    path('<uuid:project_id>/tasks/new/', views.project_task_create, name='task_create'),
    path('<uuid:project_id>/edit/', views.project_edit, name='edit'),
    path('<uuid:project_id>/cancel/', views.project_cancel, name='cancel'),
]
