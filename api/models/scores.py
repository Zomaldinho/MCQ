from operator import mod
from django.db import models
from .students import Students
from .topics import Topics

class Scores(models.Model):
    score = models.IntegerField()
    student = models.ForeignKey(Students, models.CASCADE, 'student')
    topic = models.ForeignKey(Topics, models.CASCADE, 'topic')
    
    def __str__(self):
        return f"score for student is {self.score}"