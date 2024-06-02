import time
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Contact, Email, SettingValue
from django.http import JsonResponse, StreamingHttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.contrib import messages
from django.http import HttpResponse
from googleapiclient.discovery import build
import base64
import after_response
from django.utils import timezone
import textwrap
import os

from json2html import json2html
import markdown
import html2text
import json
import re

from langchain_community.llms import Ollama
# from langchain import hub
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import Chroma
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.prompts import PromptTemplate




def contacts_view(request, contact_id=None):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        return render(request, 'email_cleaner/contacts.html', {'contacts': contacts})

    elif request.method == 'POST':
        # Handle POST request to update default activity value
        if contact_id is None:
            # If contact_id is not provided, return a bad request response
            return JsonResponse({'error': 'Contact ID is required for POST request'}, status=400)
        
        try:
            # Try to retrieve the contact by ID
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            # If contact does not exist, return a not found response
            return JsonResponse({'error': 'Contact not found'}, status=404)
        
        # Update the default activity value based on the POST data
        new_default_activity = request.POST.get('default_activity')
        if new_default_activity is not None:
            contact.default_activity = new_default_activity
            contact.save()
            return JsonResponse({'success': f'Default activity updated for contact {contact_id}'})
        else:
            return JsonResponse({'error': 'Default activity value not provided'}, status=400)

def emails_view(request):
    emails = Email.objects.all()
    is_update_emails_in_gmail_running, created = SettingValue.objects.get_or_create(setting_name="is_update_emails_in_gmail_running")
    update_emails_in_gmail_start_time, created = SettingValue.objects.get_or_create(setting_name="update_emails_in_gmail_start_time")
    is_import_from_gmail_running, created = SettingValue.objects.get_or_create(setting_name="is_import_from_gmail_running")
    import_from_gmail_running_start_time, created = SettingValue.objects.get_or_create(setting_name="import_from_gmail_running_start_time")

    if is_import_from_gmail_running.setting_value == "True":
        messages.info(request, f"Emails are being imported from gmail! Process started at {import_from_gmail_running_start_time}")

    if is_update_emails_in_gmail_running.setting_value == "True":
        messages.info(request, f"Updates are being sent to gmail! Process started at {update_emails_in_gmail_start_time}")

    is_gmail_authentication_broken, created = SettingValue.objects.get_or_create(setting_name="is_gmail_authentication_broken") 
    if is_gmail_authentication_broken.setting_value == "True":
        messages.info(request, f"Your gmail authentication is broken, please reconnect!")

    return render(request, 'email_cleaner/emails.html', 
                  {
                      'emails': emails, 
                      'is_gmail_authentication_broken': is_gmail_authentication_broken.setting_value,

                }
            )

def home_view(request):
    return render(request, 'email_cleaner/home.html')


def connect_to_gmail(request):
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    flow = InstalledAppFlow.from_client_secrets_file('email_cleaner/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('email_cleaner/token.json', 'w') as token:
        token.write(creds.to_json())

    is_gmail_authentication_broken, created = SettingValue.objects.get_or_create(setting_name="is_gmail_authentication_broken")
    is_gmail_authentication_broken.setting_value = "False"
    is_gmail_authentication_broken.save()    

    return redirect("emails")
    

def authenticate_gmail(request):
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    try:
        creds = Credentials.from_authorized_user_file('email_cleaner/token.json', SCOPES)
    except Exception as e:
        pass

    if creds and creds.valid:
        print("Authentication successful")
    else:
        is_gmail_authentication_broken, created = SettingValue.objects.get_or_create(setting_name="is_gmail_authentication_broken")
        is_gmail_authentication_broken.setting_value = "True"
        is_gmail_authentication_broken.save()
        print("Unable to authenticate with Gmail service.")
        return None

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    return service

@after_response.enable
def import_emails_from_gmail_internal(request, action_source='client_side'):
    # Connect to the Gmail API
    service = authenticate_gmail(request)
    if not(service): 
        return None
    count_emails_imported = 0

    emails_imported = []
    get_emails_from_gmail_request = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread', maxResults=100)
    
    while get_emails_from_gmail_request is not None:
        response = get_emails_from_gmail_request.execute()
        emails_imported = response.get('messages', [])
        
        for email_data in emails_imported:
            if not Email.objects.filter(external_id=email_data['id']).exists():
                msg = service.users().messages().get(userId='me', id=email_data['id'], format='full').execute()
                payload = msg['payload']
                headers = payload.get('headers')
                parts = payload.get('parts')
                body_data = parts[0].get('body', {}) if parts else payload.get('body', {})
                body_data = body_data.get('data', None)

                sender_value = next(header['value'] for header in headers if header['name'] == 'From')
                sender_contact, created = Contact.objects.get_or_create(name=sender_value, defaults={'default_activity': 'NEW'})

                # Prepare data to insert/update
                email_param = {
                    'sender': sender_contact,
                    'external_id': email_data['id'],
                    'subject': next(header['value'] for header in headers if header['name'] == 'Subject'),
                    'body': base64.urlsafe_b64decode(body_data).decode('utf-8') if body_data else None, 
                    'snippet': msg.get('snippet', ''),
                    'status': 'NEW',  
                    'auto_generated_category': None,
                    'auto_generated_summary': None,
                }

                # Insert or update into Emails table
                email_instance = Email.objects.create(**email_param)
                count_emails_imported+=1
                print("Email record inserted successfully")

        get_emails_from_gmail_request = service.users().messages().list_next(previous_request=get_emails_from_gmail_request, previous_response=response)    
    
    messages.success(request, f"{count_emails_imported} new records imported from gmail!")
    settings_to_check = [
        {"setting_name": "is_import_from_gmail_running", "default_value": "False"},
        {"setting_name": "import_from_gmail_running_last_execution_completion_time", "default_value": timezone.now().strftime("%Y-%m-%d %H:%M:%S")}
    ]

    # Check if each setting exists, and insert or update them accordingly
    for setting_data in settings_to_check:
        setting_name = setting_data["setting_name"]
        default_value = setting_data["default_value"]
        
        try:
            setting_obj = SettingValue.objects.get(setting_name=setting_name)
            # Update the setting value if it exists
            setting_obj.setting_value = default_value
            setting_obj.save()
        except SettingValue.DoesNotExist:
            SettingValue.objects.create(setting_name=setting_name, setting_value=default_value)      


def import_emails_from_gmail(request, action_source='client_side'):
    import_emails_from_gmail_internal.after_response(request, action_source)
    messages.success(request, "process initiated to import emails from gmail")

    # Settings to check
    settings_to_check = [
        {"setting_name": "is_import_from_gmail_running", "default_value": "True"},
        {"setting_name": "import_from_gmail_running_start_time", "default_value": timezone.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"setting_name": "import_from_gmail_running_last_execution_completion_time", "default_value": None}
    ]

    # Check if each setting exists, and insert or update them accordingly
    for setting_data in settings_to_check:
        setting_name = setting_data["setting_name"]
        default_value = setting_data["default_value"]
        
        try:
            setting_obj = SettingValue.objects.get(setting_name=setting_name)
            # Update the setting value if it exists
            setting_obj.setting_value = default_value
            setting_obj.save()
        except SettingValue.DoesNotExist:
            # Insert the setting if it does not exist
            SettingValue.objects.create(setting_name=setting_name, setting_value=default_value)

    if action_source == "admin_side":
        return redirect(reverse('admin:emailCleaner_email_changelist'))

    return redirect('emails')

@after_response.enable
def update_emails_in_gmail_internal(request):
    service = authenticate_gmail(request)

    emails = Email.objects.filter(status='NEW')

    count_deleted = 0
    count_marked_as_read = 0
    for email in emails:
        activity = email.sender.default_activity
        if activity == 'DELETE':
            service.users().messages().trash(userId='me', id=email.external_id).execute()
            email.status = 'DELETED'
            count_deleted+=1
            print("email deleted!")
        elif activity == 'MARK AS READ':
            service.users().messages().modify(userId='me', id=email.external_id, body={'removeLabelIds': ['UNREAD']}).execute()
            email.status = 'MARKED AS READ'
            count_marked_as_read+=1
            print("email marked as read!")
        
        email.save()
        if (count_marked_as_read + count_deleted) % 100 == 0:
            time.sleep(60)

    # Settings to check
    settings_to_check = [
        {"setting_name": "is_update_emails_in_gmail_running", "default_value": "False"},
        {"setting_name": "update_emails_in_gmail_last_execution_completion_time", "default_value": timezone.now().strftime("%Y-%m-%d %H:%M:%S")}
    ]

    # Check if each setting exists, and insert or update them accordingly
    for setting_data in settings_to_check:
        setting_name = setting_data["setting_name"]
        default_value = setting_data["default_value"]
        
        try:
            setting_obj = SettingValue.objects.get(setting_name=setting_name)
            # Update the setting value if it exists
            setting_obj.setting_value = default_value
            setting_obj.save()
        except SettingValue.DoesNotExist:
            SettingValue.objects.create(setting_name=setting_name, setting_value=default_value)    


    if (count_marked_as_read > 0) or (count_deleted > 0):
        messages.success(request, f"{count_deleted} records deleted and {count_marked_as_read} records marked as read in gmail!")


def update_emails_in_gmail(request, action_source='client_side'):
    update_emails_in_gmail_internal.after_response(request)
    messages.success(request, "process initiated to import emails from gmail")
    
    # Settings to check
    settings_to_check = [
        {"setting_name": "is_update_emails_in_gmail_running", "default_value": "True"},
        {"setting_name": "update_emails_in_gmail_start_time", "default_value": timezone.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"setting_name": "update_emails_in_gmail_last_execution_completion_time", "default_value": None}
    ]

    # Check if each setting exists, and insert or update them accordingly
    for setting_data in settings_to_check:
        setting_name = setting_data["setting_name"]
        default_value = setting_data["default_value"]
        
        try:
            setting_obj = SettingValue.objects.get(setting_name=setting_name)
            # Update the setting value if it exists
            setting_obj.setting_value = default_value
            setting_obj.save()
        except SettingValue.DoesNotExist:
            # Insert the setting if it does not exist
            SettingValue.objects.create(setting_name=setting_name, setting_value=default_value)


    if action_source == "admin_side":
        return redirect(reverse('admin:emailCleaner_email_changelist'))

    return redirect('emails')    

def clean_text(text):
    # Define the regex pattern for URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Define the regex pattern for special characters
    special_char_pattern = r'[-|"|–|”|“|*]'
    
    # Define the regex pattern for multiple spaces
    multiple_spaces_pattern = r'\s{2,}'
    
    # Remove special characters
    text = re.sub(special_char_pattern, '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(multiple_spaces_pattern, ' ', text)
    
    # Replace URLs with an empty string
    text = re.sub(url_pattern, '', text)
    
    return text

def analyze_emails_using_llm_streaming_response(request, action_source='client_side'):
    model = Ollama(model="llama3:8b-instruct-q4_0")

    template = """
    only return the json and nothing else      
    [AVAILABLE_TOOLS]
        [{"type": "function", "function": {"name": "record_auto_generated_category_and_summary", "description": "It records the generated summary and category for an email", "parameters": {"type": "object", "properties": {"category": {"type": "string", "description": "The auto generate category of the email based on the content of the email. I am product marketing specialist so I want to focus on newsletters and other types of emails where competitors are promoting there product so I can learn from it. Category of the email can be following: Newsletter, Job Alerts, Account Updates, Product Updates, Discounts/Offers."}, "blog_ideas": {"type": "string", "description": "As a product growth, I need to write content therefore suggest blog ideas from it news related to accounting or technology."}, "summary": {"type": "string", "description": "a short summary of email content. Only include the focus point in summary"}}, "required": ["category"]}}}]  
    [/AVAILABLE_TOOLS]    
    [FORMAT INSTRUCTIONS]
        return data in valid json, 
        only return the json and nothing else 
        json output example is following;
        "category": "?",
        "summary": "?",
        "blog_ideas": "?"

    [/FORMAT INSTRUCTIONS]
    [INST] 
        You are an AI language model trained to understand and summarize email content. The goal is to extract a concise summary of the email's focus points. Specifically, as a product growth consultant, I need to generate blog ideas related to accounting or technology news based on the email content.
        always use the tool.
        
        1. Extract the Summary:
        - Read the email and identify the main focus points.
        - Summarize the key points in a concise manner.
        - Ensure the summary includes only the most relevant information.

        2. Generate Blog Ideas:
        - Based on the email content, suggest three to five blog ideas.
        - The blog ideas should be related to accounting or technology news.
        - Ensure that the ideas are relevant, engaging, and could provide value to readers interested in accounting or technology.

        return data in valid json for the tool, 
                                  
        # example of categorization
        subject | category |
        Your Google data is ready to download | Account Updates |
        Welcome to the Google Developer Program | Account Updates |
        Last chance to register for UiPath Live: The Need for Speed | Product Updates |
        Accountant / Accounts Officer, PRODIGY at PRODIGY and 1+ new jobs on ACCA Careers | Job Alerts |
        Azfar Bukhari, New Value Solutions may want to hire you | Job Alerts |
        Why your practice needs a real-time data strategy and how to get there. | Newsletter | 
        NEW! Meta Data Analytics Professional Certificate | Discount/Offers | 
        UBL Digital App: Successfully Logged-in | Account Updates | 
        UBL Digital: Device Registration | Account Updates | 
        anything from XU magazine is a newsletter, XU magazine emails should not be deleted. 


        # sender
        {sender}

        # subject
        {subject}

        # snippet
        {snippet}

        # email content 
        {body}
                                
    [/INST]
    only return the json and nothing else.
    """

    result = ""
    count_of_emails = 0
    for email_data in Email.objects.exclude(status='DELETED').filter(auto_generated_category="TO BE DEFINED"):

        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = True  
        markdown_converter.ignore_images = True  
        markdown_converter.ignore_emphasis = True
        
        email_body_markdown_shorten = ""

        if email_data.body: 
            email_body_links_removed = clean_text(email_data.body)
            email_body_markdown = markdown_converter.handle(email_body_links_removed)
            if len(email_body_markdown) > 1001:
                email_body_markdown_shorten = email_body_markdown[:1000]
            else:
                email_body_markdown_shorten = email_body_markdown
        
        my_prompt = template.replace("{sender}", email_data.sender.name or "").replace("{subject}", email_data.subject or "").replace("{snippet}", email_data.snippet or "").replace("{body}", email_body_markdown_shorten or "")
        response_from_llm = model.invoke(my_prompt)

        # response_from_llm = "paused"
        print("#" * 10)
        print(response_from_llm)
        
        response_from_llm_dict = {}
        try:
            response_from_llm_dict = json.loads(response_from_llm)
            email_data.auto_generated_category  = response_from_llm_dict['category']
            email_data.auto_generated_summary =  response_from_llm_dict['summary'] 
            email_data.auto_generated_blog_ideas = response_from_llm_dict.get('blog_ideas', "")
            email_data.save()
        except Exception as e:
            email_data.auto_generated_category  = "ERROR"
            email_data.auto_generated_summary = str(e) + str(response_from_llm_dict if response_from_llm_dict else "") 
            email_data.save()            



        my_prompt_prettified = markdown.markdown(my_prompt)
        try:
            response_from_llm_prettified =  json2html.convert(response_from_llm_dict if response_from_llm_dict else response_from_llm)
        except:
            response_from_llm_prettified = response_from_llm

        count_of_emails+=1
        yield f'<h1>Email {count_of_emails}</h1><h2>INPUT </h2> <div style="max-width:50%;word-break: break-all; white-space: normal;">{my_prompt_prettified}</div> <hr> <h2>LLM RESPONSE</h2> <div style="max-width:100%; word-wrap:break-word;">{response_from_llm_prettified}</div> <hr><hr><hr>'
        
        if count_of_emails == 1000:
            break 
        

def analyze_emails_using_llm_internal(request, action_source='client_side'):
    response = StreamingHttpResponse(render(request, "email_cleaner/emails_analysis.html"), content_type='text/html')
    response.streaming_content = analyze_emails_using_llm_streaming_response(request, action_source='client_side')
    return response