# Generated by Django 4.2.13 on 2024-05-27 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0005_task_external_links'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['due_date_time']},
        ),
    ]