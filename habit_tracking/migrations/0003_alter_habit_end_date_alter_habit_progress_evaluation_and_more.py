# Generated by Django 4.1 on 2024-03-26 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "habit_tracking",
            "0002_alter_habit_description_alter_habit_end_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="habit",
            name="progress_evaluation",
            field=models.CharField(
                choices=[
                    ("yes_no", "Yes or No"),
                    ("numeric", "Numeric Value"),
                    ("timer", "Timer"),
                ],
                default="yes_no",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="habit",
            name="target_definition",
            field=models.CharField(
                choices=[
                    ("at_least", "At least"),
                    ("less_than", "Less than"),
                    ("exactly", "Exactly"),
                    ("any_value", "Any value"),
                ],
                default="at_least",
                max_length=100,
            ),
        ),
    ]
