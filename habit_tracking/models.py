from django.db import models
from django.contrib.auth.models import User
from core.models import FREQUENCY_CHOICES

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=[(i, i) for i in range(1, 11)], default=5)  
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    progress_evaluation = models.CharField(max_length=20, choices=[
        ('yes_no', 'Yes or No'),
        ('numeric', 'Numeric Value'),
        ('timer', 'Timer'),
    ], default='yes_no')

    target_definition = models.CharField(max_length=100, choices=[
        ('at_least', 'At least'),
        ('less_than', 'Less than'),
        ('exactly', 'Exactly'),
        ('any_value', 'Any value'),
    ], default='at_least')
    
    daily_goal_numeric = models.FloatField(null=True, blank=True)
    weekly_goal_numeric = models.FloatField(null=True, blank=True)
    monthly_goal_numeric = models.FloatField(null=True, blank=True)
    yearly_goal_numeric = models.FloatField(null=True, blank=True)
    single_time_goal_numeric = models.FloatField(null=True, blank=True)

    daily_goal_duration = models.DurationField(null=True, blank=True)
    weekly_goal_duration = models.DurationField(null=True, blank=True)
    monthly_goal_duration = models.DurationField(null=True, blank=True)
    yearly_goal_duration = models.DurationField(null=True, blank=True)
    single_time_goal_duration = models.DurationField(null=True, blank=True)

    unit = models.CharField(max_length=50, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="daily")

    def __str__(self):
        return self.name

class HabitLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    completion_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ], default='pending')
    progress_duration = models.DurationField(null=True, blank=True)
    progress_numeric = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date}: {self.habit.name} - Status: {self.completion_status}"
