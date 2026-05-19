from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('new/', views.task_create, name='create'),
    path('<int:task_id>/edit/', views.task_edit, name='edit'),
]
