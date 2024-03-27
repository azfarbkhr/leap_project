from django.contrib import admin
from .models import JournalEntry

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'log_preview', 'created_at', 'habit', 'category', 'sentiment')
    list_filter = ('user', 'created_at', 'habit', 'category', 'sentiment')
    search_fields = ('user__username', 'log', 'habit__name', 'category__name')

    def log_preview(self, obj):
        return obj.log[:50] + '...' if len(obj.log) > 50 else obj.log
    log_preview.short_description = 'Log Preview'

