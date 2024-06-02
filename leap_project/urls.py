"""leap_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('massadmin.urls')),
    path("admin/", admin.site.urls),
    path('', include('core.urls')),
    path('financial-tracking/', include('financial_tracking.urls')),
    path('task-management/', include('task_management.urls')),
    path('habit-tracking/', include('habit_tracking.urls')),
    path('journaling/', include('journaling.urls')),
    path('time-tracking/', include('time_tracking.urls')),
    path('email-cleaner/', include('email_cleaner.urls')),
        
]
