from django.db import models
from django.contrib.auth.models import User

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('core.Category', on_delete=models.SET_NULL, null=True, blank=True)
    habit = models.ForeignKey('habit_tracking.Habit', on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('core.Project', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Time Entry by {self.user.username}: ({self.start_time})"

    class Meta:
        verbose_name = "Time Entry"
        verbose_name_plural = "Time Entries"