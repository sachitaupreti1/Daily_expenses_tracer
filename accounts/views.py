from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

# Dashboard view


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "accounts/dashboard.html")

# Login view


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, "accounts/login.html")

# Register view (placeholder)


def register(request):
    return render(request, "accounts/register.html")

# Logout view


def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('login')
    return render(request, "accounts/logout.html")
