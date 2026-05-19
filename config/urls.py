from django.contrib import admin
from django.urls import include, path
from accounts.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('project/', include('project.urls')),
    path('tasks/', include('tasks.urls')),
]
