from django.contrib.auth.models import User
from django.db import models

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('daily_workdays', 'WeekDays Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reminder_time = models.DateTimeField()
    habit = models.ForeignKey('habit_tracking.Habit', on_delete=models.CASCADE, null=True, blank=True)
    budget_period = models.ForeignKey('financial_tracking.BudgetingPeriod', on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey('task_management.Task', on_delete=models.CASCADE, null=True, blank=True)
    time_entry = models.ForeignKey('time_tracking.TimeEntry', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Reminder at {self.reminder_time}"
    
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
