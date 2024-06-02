from django.contrib import admin
from .models import Contact, Email, SettingValue
from .views import update_emails_in_gmail, import_emails_from_gmail


@admin.action(description='Set default activity to DELETE')
def set_default_activity_delete(modeladmin, request, queryset):
    queryset.update(default_activity='DELETE')

@admin.action(description='Set default activity to MARK AS READ')
def set_default_activity_mark_as_read(modeladmin, request, queryset):
    queryset.update(default_activity='MARK AS READ')

@admin.action(description='Export emails based on default activity')
def update_emails_in_gmail_action(modeladmin, request, queryset):
    return update_emails_in_gmail(request, action_source='admin_side')


@admin.action(description='Import emails from gmail')
def import_emails_from_gmail_action(modeladmin, request, queryset):
    return import_emails_from_gmail(request, action_source='admin_side')


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_email_count', 'default_activity', )
    list_filter = ('default_activity',)
    inlines = [EmailInline]
    list_editable = ('default_activity',)
    search_fields = ('name',)
    actions = [set_default_activity_delete, set_default_activity_mark_as_read]

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'sender', 'subject', 'status','sender_default_activity', 'auto_generated_category')
    list_filter = ('status', 'auto_generated_category', 'sender')
    search_fields = ('subject', 'snippet', 'body', 'external_id')
    raw_id_fields = ('sender',)
    massadmin_exclude = ['external_id', 'sender', 'subject', ]
    actions = [update_emails_in_gmail_action]

    def sender_default_activity(self, obj):
        return obj.sender.default_activity if obj.sender else None
    sender_default_activity.short_description = 'Expected Activity'


@admin.register(SettingValue)
class SettingValueAdmin(admin.ModelAdmin):
    list_display = ('setting_name', 'setting_value')