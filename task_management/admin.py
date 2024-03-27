from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('details', 'category', 'project', 'urgency', 'business_value', 'priority', 'favorite', 'is_added_to_my_day', 'due_date_time', 'task_completion_status')
    list_filter = ('category', 'project', 'urgency', 'business_value', 'priority', 'favorite', 'is_added_to_my_day', 'task_completion_status')
    search_fields = ('details',)
    date_hierarchy = 'due_date_time'
