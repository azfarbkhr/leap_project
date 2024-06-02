from django.db import models
from django.contrib.auth.models import User
from core.models import FREQUENCY_CHOICES

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    category = models.ForeignKey('core.Category', on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('core.Project', on_delete=models.SET_NULL, null=True, blank=True)
    urgency = models.CharField(max_length=20, choices=[
        ('1', 'Immediate'),
        ('2', 'Day End'),
        ('3', 'Week End'),
        ('4', 'Month End'),
        ('5', 'No Deadline'),
    ], default='5')

    priority = models.IntegerField(choices=[(i, i) for i in range(1, 11)], default=5)  
    business_value = models.IntegerField(choices=[(i, i) for i in range(1, 11)], default=5)  
    favorite = models.BooleanField(default=False)
    is_added_to_my_day = models.BooleanField(default=False)
    
    dependent_on_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dependent_tasks')
    to_be_completed_before_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subsequent_tasks')
    
    closed_date = models.DateTimeField(null=True, blank=True)
    task_completion_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('skipped', 'Skipped'),
        ('done', 'Done'),
        ('parked', 'Parked'),
    ], default='pending')
    
    due_date_time = models.DateTimeField(null=True, blank=True)
    planned_time_in_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    planned_start_date_time = models.DateTimeField(null=True, blank=True)
    planned_start_date_calculation_type = models.CharField(max_length=20, choices=[
        ('fixed_date', 'Fixed Date'), 
        ('dependent_date', 'Dependent Date')
    ], default='fixed_date')

    close_task_after = models.DurationField(null=True, blank=True)
    progress_status_on_closure = models.CharField(max_length=255, blank=True, choices=[
        ('pending', 'Pending'),
        ('skipped', 'Skipped'),
        ('done', 'Done'),
        ('parked', 'Parked'),
    ], default='parked')

    post_actions_on_closure = models.CharField(max_length=255, blank=True, choices=[
        ('new_task', 'Create a new task'),
    ], default='new_task')

    repeat_frequency = models.CharField(max_length=20, blank=True, choices=FREQUENCY_CHOICES)
    
    # allow user to store multiple external links seperated by | character
    external_links = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.details

    class Meta:
        ordering = ['due_date_time']

