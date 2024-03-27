from django.contrib import admin
from .models import Category, Reminder, Project

admin.site.site_header = 'Leap Project Admin'
admin.site.site_title  = 'Leap Project'
admin.site.index_title  = 'Admin'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit', 'reminder_time')
    search_fields = ('user__username',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)