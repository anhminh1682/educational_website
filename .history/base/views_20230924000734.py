from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'home.html')

def classes(request):
    return render(request, 'classes.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')  # lấy từ file login.html
        password = request.POST.get('password')  # lấy từ file login.html
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Email hoặc mật khẩu không chính xác!')
    context = {'user_not_login': "show",
               'user_login': "hidden"}
    return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def detail(request):
    return render(request, 'detail.html')