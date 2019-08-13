from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
import json
from random import randint
from django.db.models import Min,Max
from .models import Task

# Create your views here.



def table(request):
    try:
        print('refreshing updates: '+ str(refreshTasks()))
        LastUpdated = datetime.now()
    except:
        LastUpdated = 'Couldn\'t update'
    context = {'Task':Task.objects.all(), 'LastUpdated' : LastUpdated}
    return HttpResponse(render(request, 'taskbrowser/table.html',context))

def get_task(request, task_id):

    if request.method == 'GET':
        try:
            mytask = Task.objects.get(id= task_id)
            payload = json.dumps([{"Task": mytask.Name, "Task Owner": mytask.taskowner, "Priority":mytask.priority}])
            status = 200
        except:
            payload = json.dumps([{"Error" : "Task not found."}])
            status=404
    else:
        payload='Expecting GET request, unexpected behaviour received.'
        Status = 400

    return HttpResponse(payload, content_type='text/json',status=status)

def refreshTasks():
    #for all NULL tasks
    for parentTask in Task.objects.filter(P=''):
        #for child tasks
        recurseChild(Task.objects.filter(P=parentTask.id), parentTask)

def recurseChild(ChildTasks, parentTask):
    Status = 'Idle'    
    #Check if object has  children
    if Task.objects.filter(P=parentTask.id):
        #I've got children
        for child in Task.objects.filter(P=parentTask.id):
            recurseChild(Task.objects.filter(P=parentTask.id),child)
        
        runs =Task.objects.filter(P=parentTask.id, Status = 'Running').count()
        schedules = Task.objects.filter(P=parentTask.id, Status = 'Scheduled').count()
        completes = Task.objects.filter(P=parentTask.id, Status = 'Complete').count()
        
        if runs > 1:
            Status = 'Multi-Runs'
        elif runs == 1:
            Status = 'Running'
        elif schedules > 0 and completes == 0:
            Status = 'Scheduled'
        else:
            Status = 'Idle'
        Task(Status=Status,id=parentTask.id,P=parentTask.P,Name=parentTask.Name,StartDate=ChildTasks.aggregate(Min('StartDate'))['StartDate__min'],EndDate=ChildTasks.aggregate(Max('EndDate'))['EndDate__max']).save()
    else:
        #print("I've got no children")        
        if parentTask.StartDate > timezone.now():
            Status = 'Scheduled'
        elif parentTask.StartDate < timezone.now() and parentTask.EndDate > timezone.now():            
            Status = 'Running'
        else:
            Status = 'Complete'
        Task(id=parentTask.id,Name=parentTask.Name,StartDate=parentTask.StartDate,EndDate=parentTask.EndDate,P=parentTask.P,Status = Status).save()


