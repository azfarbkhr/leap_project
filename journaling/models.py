from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    habit = models.ForeignKey('habit_tracking.Habit', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('core.Category', on_delete=models.SET_NULL, null=True, blank=True)    
    sentiment = models.CharField(max_length=20, choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('angry', 'Angry'),
        ('excited', 'Excited'),
    ])

    def __str__(self):
        return f"Journal Entry by {self.user.username} at {self.created_at}"
