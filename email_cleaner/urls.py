from django.urls import path, re_path
from .views import contacts_view, emails_view, home_view, import_emails_from_gmail, update_emails_in_gmail, analyze_emails_using_llm_internal, connect_to_gmail

urlpatterns = [
    path('', home_view, name='email_cleaner_dashboard'),
    path('emails/', emails_view, name='emails'),
    path('import_emails_from_gmail', import_emails_from_gmail, name='import_emails_from_gmail'),
    path('update_emails_in_gmail', update_emails_in_gmail, name='update_emails_in_gmail'),
    path('analyze_emails_using_llm_internal', analyze_emails_using_llm_internal, name='analyze_emails_using_llm_internal'),
    path('connect_to_gmail', connect_to_gmail, name='connect_to_gmail'),
    re_path(r'^contacts(?:/(?P<contact_id>\d+))?/$', contacts_view, name='contacts'),
    

]
