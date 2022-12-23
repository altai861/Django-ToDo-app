from django.shortcuts import render
from django.http  import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Task
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

@login_required
def update_task(request, task_id):
    task = Task.objects.filter(id = task_id)
    if request.method == "GET":
        return render(request, "update_task.html", {
            "tasks":task
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        try:
            complete = request.POST["complete"]
            if complete == "on":
                comp = True
        except MultiValueDictKeyError:
            comp = False
            
        task.update(title=title, description=description, complete=comp)
        return HttpResponseRedirect(reverse('tasks'))


@login_required
def delete_task(request, task_id):
    if request.method == "GET":
        task = Task.objects.filter(id = task_id)
        return render(request, "delete_task.html", {
            "tasks" : task
        })
    else:
        task = Task.objects.filter(id = task_id)
        print(task)
        task.delete()
        return HttpResponseRedirect(reverse('tasks'))


@login_required
def view_task(request, task_id):
    task = Task.objects.filter(id = task_id)
    return render(request, 'view_task.html', {
        "task" : task
    })


@login_required
def add_task(request):
    if request.method == "GET":
        return render(request, "add_task.html")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        task = Task(user=request.user, title=title, description=description)
        task.save()
        return HttpResponseRedirect(reverse('tasks'))



def tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        return render(request, "tasks.html", {
            "tasks": tasks
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tasks"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("tasks"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Username address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("tasks"))
    else:
        return render(request, "register.html")
