from unicodedata import name
from django.db import models

class Students(models.Model):
    name = models.CharField(max_length=100, blank=False)
    age = models.IntegerField(blank=False)
    phone_number =  models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.name}"