import uuid
from django.db import models
from datetime import datetime

# Create your models here.
class Task(models.Model):
    #use django std lib to generate unique id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    #name to be given at point of generation
    Name = models.CharField(max_length=18)
    #explicitly declare parent of object at point of generation
    P = models.TextField()
    #variables for status choices
    a,b,c,d,e = ['Scheduled','Running','Complete','Multi-Runs','Idle']
    status_choices = [(a,a),(b,b),(c,c),(d,d),(e,e)]
    Status = models.CharField(max_length=10, choices=status_choices)
    #date and time scheduled
    StartDate = models.DateTimeField(null='true',auto_now=False,auto_now_add=False)
    #date and time it will finish
    EndDate = models.DateTimeField(null='true',auto_now=False,auto_now_add=False)
    taskowner = models.CharField(editable=True,default='noowner',max_length=30)
    priority = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.Name)