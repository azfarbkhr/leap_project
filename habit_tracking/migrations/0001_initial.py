# Generated by Django 4.1 on 2024-03-26 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "priority",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                        ]
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "target_definition",
                    models.CharField(
                        choices=[
                            ("at_least", "At least"),
                            ("less_than", "Less than"),
                            ("exactly", "Exactly"),
                            ("any_value", "Any value"),
                        ],
                        max_length=100,
                    ),
                ),
                ("goal_duration", models.DurationField(blank=True, null=True)),
                ("goal_numeric", models.FloatField(blank=True, null=True)),
                (
                    "progress_evaluation",
                    models.CharField(
                        choices=[
                            ("yes_no", "Yes or No"),
                            ("numeric", "Numeric Value"),
                            ("timer", "Timer"),
                        ],
                        max_length=20,
                    ),
                ),
                ("weekly_goal", models.FloatField(blank=True, null=True)),
                ("monthly_goal", models.FloatField(blank=True, null=True)),
                ("yearly_goal", models.FloatField(blank=True, null=True)),
                ("single_time_goal", models.FloatField(blank=True, null=True)),
                ("unit", models.CharField(blank=True, max_length=50)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("daily", "Daily"),
                            ("weekly", "Weekly"),
                            ("monthly", "Monthly"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.category"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
