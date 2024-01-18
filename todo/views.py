from django.shortcuts import render , redirect,get_object_or_404
from django.db import IntegrityError
from .models import Task,CustomUser
from django.http import HttpResponse,HttpResponseBadRequest, HttpResponseForbidden
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# Create your views here.

def signup(request):
    templates = loader.get_template('signup.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'signup.html', {'error': "Username or password IS REQUIRED"})
        else:
             pass
        try:
            CustomUser.objects.create(username=username, password=password)
        except IntegrityError:
            return render(request, 'signup.html', {'error': f"Username \"{username}\" Already Exists" })
        
        # return HttpResponse(templates.render({'success': f"Dear {username}, Your account has been created"}, request))
        return redirect('login')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'login.html', {'error': "Username and password IS REQUIRED"})
        else:
             pass
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': "Invalid username or password"})
            # Checking if the password matches the password for the username
        if user.password == password:
            request.session['logged_in_user'] = username
            # this will help when the redirecting url has a parameter 'next'
            new_redirect = request.GET.get('next', 'login_home') 
            return redirect(new_redirect)
        else:
            return render(request ,'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html') 



def user_logout(request):
    logout(request)
    return redirect('login')

def test(request):
    pass

def dbd(request):
    if 'logged_in_user' in request.session:
        username = request.session['logged_in_user']
        try:
            user = CustomUser.objects.get(username=username)
            todos = Task.objects.filter(owner=user)
            for x in todos:
                if x.completed == True:
                    x.completed = 'Completed'
                else:
                    x.completed = 'Not Completed'
            return render(request, 'dashb.html', {'tasks': todos, 'user': user})
        except CustomUser.DoesNotExist:
            pass
    else:
         templates = loader.get_template('login.html')
         context ={
             'log_error': 'You must login to access this page'
         }
         return HttpResponse(templates.render(context, request))
        # return render(request ,'login', {'log_error': 'You must login to access this page'})
        # return redirect('login')  # Redirect to the login page if not logged in


def add_task(request):
    if 'logged_in_user' in request.session:
        username = request.session['logged_in_user']
        user = CustomUser.objects.get(username=username)
        if request.method == 'POST':
            task_name = request.POST['task_name']
            tasks_description = request.POST['task_description']
            task_complete = request.POST['task_complete']
            new_task = Task.objects.create(owner=user, name=task_name, description=tasks_description, completed=task_complete,created_at=datetime.now())
            
            return redirect('home')
        return render(request, 'add_task.html')

def delete_task(request, task_id):
    if 'logged_in_user' in request.session:
        username = request.session['logged_in_user']
        try:
            user = CustomUser.objects.get(username=username)
            # Ensure the task belongs to the logged-in user
            task = get_object_or_404(Task, id=task_id, owner=user)
            # Delete the task
            task.delete()
        except (CustomUser.DoesNotExist, Task.DoesNotExist):
            # Handle case where the user or task does not exist
            pass

    return redirect('home')


def update_task(request, task_id):
    if 'logged_in_user' in request.session:
        username = request.session['logged_in_user']
        try:
            user = CustomUser.objects.get(username=username)
            task = get_object_or_404(Task, id=task_id, owner=user)
            
            if request.method == 'POST':
                task.name = request.POST['task_name']
                task.description = request.POST['task_description']
                task.completed = request.POST['task_complete']
                task.save()
                return redirect('home')
            
            return render(request, 'update_task.html', {'task': task})
        
        except CustomUser.DoesNotExist:
            return render(request, 'update_task.html', {'update_task': 'An error occurred'})
    
    return redirect('login')  # Redirect to login if user is not logged in or doesn't have permission

def link_update_task(request, task_id):
    if 'logged_in_user' in request.session:
        return redirect('update_tasks')