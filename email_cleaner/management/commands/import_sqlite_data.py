# your_app/management/commands/import_from_sqlite.py

import sqlite3
from django.core.management.base import BaseCommand
from email_cleaner.models import Contact, Email, SettingValue
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class Command(BaseCommand):
    help = 'Import data from an external SQLite file into the local Django database'

    def handle(self, *args, **kwargs):
        # Path to the external SQLite file
        external_db_path = BASE_DIR / 'db2.sqlite3'

        # Connect to the external SQLite database
        conn = sqlite3.connect(external_db_path)
        cursor = conn.cursor()

        # Import Contact data
        cursor.execute("SELECT id, name, default_activity FROM emailCleaner_contact")
        contacts = cursor.fetchall()
        for contact in contacts:
            Contact.objects.update_or_create(
                id=contact[0],
                defaults={'name': contact[1], 'default_activity': contact[2]}
            )

        # Import Email data
        cursor.execute("SELECT id, external_id, sender_id, subject, body, snippet, status, auto_generated_category, auto_generated_summary, auto_generated_blog_ideas FROM emailCleaner_email")
        emails = cursor.fetchall()
        for email in emails:
            Email.objects.update_or_create(
                id=email[0],
                defaults={
                    'external_id': email[1],
                    'sender_id': email[2],
                    'subject': email[3],
                    'body': email[4],
                    'snippet': email[5],
                    'status': email[6],
                    'auto_generated_category': email[7],
                    'auto_generated_summary': email[8],
                    'auto_generated_blog_ideas': email[9]
                }
            )

        # Import SettingValue data
        cursor.execute("SELECT id, setting_name, setting_value FROM emailCleaner_settingvalue")
        settings = cursor.fetchall()
        for setting in settings:
            SettingValue.objects.update_or_create(
                id=setting[0],
                defaults={'setting_name': setting[1], 'setting_value': setting[2]}
            )

        # Close the connection
        conn.close()

        self.stdout.write(self.style.SUCCESS('Successfully imported data from external SQLite database'))
