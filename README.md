# TaskTrees

TaskTrees is a task browser built with the django framework.
Each task has the following attributes
```yaml
    - id = Each Task has a unique id. uuid was used to generate unique hash values for each task
    - Start Date = Scheduled start date and time for the given task
    - End Date = Scheduled finish time for given task
    - Status = Current status of the task indicating whether it's running, scheduled or complete
    - Parent = Parent task, if the task is a sub task of another task
    - Task owner = Task owned by which person
    - Priority = Task Priority
```
The framework displays a table of all tasks on a rendered web-page.

Given DB has following tree structure
```yaml
Task A:
    Task A1
Task B:
    Task B1
    Task B2
Task C:
    Task C1
    Task C2
    Task C3:
        Task C3b
Task D:
    Task D1
```


## Installation

Simply clone this directory onto a folder of yours. 
You need python and django installed. Use pip for django
```bash
git clone https://github.com/sahilabro/tasktrees
cd <taskbrowser-directory>
python manage.py makemigrations
python manage.py migrate
python runserver <insert where you want it deployed>
```
check localhost:8000 or wherever you deployed it to see the table.

## Status

The status of a parent task depends on its sub tasks.
A parent task status can be:

    - Scheduled: If none of its sub tasks have run yet
    - Running: If one of its sub tasks are running
    - Multi-Runs: If multiple sub tasks are running
    - Idle: If no sub tasks are running, but one or more are scheduled, and one or more are completed

The status of tasks with no sub tasks is called an actual task. An actual task cannot be 'idle,' it can be one of the following:
    - Scheduled
    - Running
    - Completed

## Back-end for Tree recursion

There is no limit on how many dependencies a sub task can have, as sub tasks can have their own sub tasks with no limitations. 

This is a typical traversing trees problem. The status for each task needs to be worked out by looking at its sub-tasks. This process is to be repeated until the sub-task has no children tasks. It was chosen not to update the database at given intervals - rather they will update whenever a request is made to the web-page - i.e. when our function in views.py is triggered through regular expression and url matching.

A request to the web-page makes a call to the refreshTasks() function. Psuedocode to represent recursion used:

```python
 for parentTask in ListOfTasksWithNoParent:
        recurseChild(listOfChildTasksForGivenParentTask, parentTask)
```

Recursion function:

```python
def recurseChild(ChildTasks, parentTask):
    if parentTaskHasChildren:
        for childtask in parentTask:
            #recurse until childtask has no children tasks.
            recurseChild(listOfChildTasksForGivenChildTask,childtask)
        #code
        #code to work out status of parents by looking at status of children here
    else:
        #code
        #code to work out status of actual child tasks with no dependencies
```

Please note that while this is a good solution for occasional use, it is bad if multiple users make calls at the same time, as the function creates update and save SQL queries to the backend for each call. A query scheduler would have to be implemented if the table were to be viewed frequently by multiple users.

This solution is more efficient if intended for a single user, or if the calls made are spaced apart as it eliminated the need for a scheduler.


## RESTful API

A restful api was built to query a task for its priority and task owner. The api can be accessed by the /api/ prefix followed by the task id.

In our urls.py file we map anything prefixed by /api/ onto a variable called task_id. This is passed onto views.py which processes the GET call:

urls.py
...
```python
path('api/<str:task_id>', views.get_task)
```
...

The get_task function in views.py makes SQL queries into the backend database to find a matching task id, if it finds it will return the task owner and priority in a json file - or it will raise an error.

Try it (make sure server is running) by going to 

localhost:8000/297a1327-8780-4f95-9fe3-004ba4d9d406

For TaskA, for given arbitrary database in the repository.

## Front-end

I used bootstrap css and js modules to add colours and hover-over attributes to the table. This is done easily as the webpages are rendered using html templates within django. The templates can be applied to multiple tables, if we were to map our application onto multiple streams urls in the future.

