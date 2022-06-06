from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo

# Create your views here.


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, "todo/currenttodos.html", {"todos": todos})


def home(request):
    return render(request, "todo/home.html")


def signupuser(request):
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("home")
            except IntegrityError:
                return render(
                    request,
                    "todo/signupuser.html",
                    {"form": UserCreationForm(), "error": "Username already exists."},
                )
        else:
            return render(
                request,
                "todo/signupuser.html",
                {"form": UserCreationForm(), "error": "Passwords did not match."},
            )


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/loginuser.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "todo/loginuser.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username and password did not match.",
                },
            )
        else:
            login(request, user)
            return redirect("home")


def createtodo(request):
    if request.method == "GET":
        return render(request, "todo/createtodo.html", {"form": TodoForm()})
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return render(request, "todo/home.html")
