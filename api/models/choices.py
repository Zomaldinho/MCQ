from django.db import models

from .questions import Questions
from .topics import Topics

class Choices(models.Model):
    text = models.CharField(max_length=400)
    question = models.ForeignKey(Questions, models.CASCADE, related_name='choices')
    is_answer = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['?']
    
    def __str__(self):
        return f"{self.text}"