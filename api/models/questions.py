from django.db import models

from .topics import Topics

class Questions(models.Model):
    text = models.CharField(max_length=300)
    topic = models.ForeignKey(Topics, models.CASCADE)
    
    class Meta:
        ordering = ['?']
    
    def __str__(self):
        return f"{self.text}"