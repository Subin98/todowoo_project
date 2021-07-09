from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import todoform
from .models import todo
from django.utils import timezone

# signup
def signupuser(request):

    if request.method == 'GET':
        return render(request, 'todo/signupuser.html',{'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',{'form':UserCreationForm,'error':'User name already taken'})

        else:
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm,'error':'passwords doesnot match'})

#currenttodos
def currenttodos(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    else:
        todos=todo.objects.filter(user=request.user, datecompleted__isnull=True)
        return render(request,'todo/currenttodos.html',{'todos':todos})

def completedtodos(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    else:
        todos=todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        return render(request,'todo/completedtodos.html',{'todos':todos})

#logout
def logoutuser(request):
    if request.method== 'POST':
        logout(request)
        return redirect('home')

#loginuser

def loginuser(request):
    #if request.user.is_authenticated:
        #return redirect('currenttodos')
    if request.method == 'GET':
        return render(request, 'todo/login.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html',{'form':AuthenticationForm,'error':'user name or password is incorrect'})
        else:
            login(request,user)
            return redirect('currenttodos')



def home(request):
    return render(request,'todo/home.html')
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':todoform()})
    else:
        try:
            form=todoform(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user=request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',{'form':todoform(), 'error':"Bad data"})


#edittodo

def editodo(request, todo_pk):
    Todo=get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form=todoform(instance=Todo)
        return render(request,'todo/editodo.html', {'Todo':Todo, 'form':form})
    else:
        try:
            form=todoform(request.POST, instance=Todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/editodo.html',{'form':form, 'error':"Bad data"})


def completetodo(request, todo_pk):
    Todo=get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        Todo.datecompleted=timezone.now()
        Todo.save()
        return redirect('currenttodos')

def deletetodo(request, todo_pk):
    Todo=get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        Todo.delete()
        return redirect('currenttodos')
