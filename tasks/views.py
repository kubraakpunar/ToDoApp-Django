from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print("Görev başarıyla kaydedildi.")
        else: 
            print("Form geçersiz:",form.errors)
        return redirect('/')
    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)

@login_required
def updateTask(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)

@login_required
def deleteTask(request, pk):
    item = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'tasks/delete.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

