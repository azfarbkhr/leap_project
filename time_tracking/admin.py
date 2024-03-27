from django.contrib import admin
from .models import TimeEntry

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'habit', 'project', 'notes', 'start_time', 'end_time', 'duration')
    list_filter = ('user', 'category', 'habit', 'project')
    search_fields = ('user__username', 'notes', 'project__name')