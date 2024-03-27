# habit_tracking/admin.py

from django.contrib import admin
from .models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'priority', 'start_date', 'end_date', 'frequency')
    list_filter = ('user', 'category', 'priority', 'frequency')
    search_fields = ('name', 'description')

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit', 'date', 'completion_status', 'progress_duration', 'progress_numeric', 'notes')
    list_filter = ('user', 'habit', 'date', 'completion_status')
    search_fields = ('habit__name', 'notes')
