from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404
from todolist.forms import TaskForm
from .models import Task

# Create your views here.
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')

    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = HttpResponseRedirect(
                reverse("todolist:show_todolist"))  
            response.set_cookie('last_login', str(datetime.datetime.now()))
            response.set_cookie('username', username)
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    response.delete_cookie('username')
    return response

@login_required(login_url='/todolist/login/')
def show_todolist(request):
    tasks = Task.objects.filter(user=request.user).order_by('id')
    context = {
        'username': request.COOKIES['username'],
        'last_login': request.COOKIES['last_login'],
        'tasks': tasks,
    }
    return render(request, "todolist.html", context)

@login_required(login_url='/todolist/login/')
def create_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return HttpResponseRedirect(reverse('todolist:show_todolist'))
    
    context = {'form': TaskForm()}
    return render(request, 'create_task.html', context)

@login_required(login_url='/todolist/login/')
def delete_task(request, id):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=id, user=request.user)
        task.delete()

        return redirect(reverse('todolist:show_todolist'))

@login_required(login_url='/todolist/login/')
def update_status(request, id):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=id, user=request.user)
        task.is_finished = not task.is_finished
        task.save()

        return redirect(reverse('todolist:show_todolist'))