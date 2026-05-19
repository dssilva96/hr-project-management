from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='list'),
    path('new/', views.employee_create, name='create'),
    path('<uuid:employee_id>/edit/', views.employee_edit, name='edit'),
    path('<uuid:employee_id>/deactivate/', views.employee_deactivate, name='deactivate'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/new/', views.team_create, name='team_create'),
    path('teams/<uuid:team_id>/', views.team_detail, name='team_detail'),
    path('teams/<uuid:team_id>/edit/', views.team_edit, name='team_edit'),
]
