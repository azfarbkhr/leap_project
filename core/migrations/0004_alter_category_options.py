# Generated by Django 4.1 on 2024-03-26 22:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_reminder_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
    ]
