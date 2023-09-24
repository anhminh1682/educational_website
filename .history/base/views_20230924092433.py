from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def get_common_context(request):
    context = {'user_not_login': "show", 'user_login': "hidden"}
    if request.user.is_authenticated:
        context = {'user_not_login': "hidden", 'user_login': "show"}
    return context

def home(request):
    context = {'user_not_login': "show",
               'user_login': "hidden"}
    if request.user.is_authenticated:
        return  render(request, 'home.html', context)
    else:
        context = {'user_not_login': "hidden",
               'user_login': "show"}
    return render(request, 'home.html', context)

def classes(request):
    return render(request, 'classes.html')

def loginPage(request):
    context = {'user_not_login': "show",
               'user_login': "hidden"}
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')  # lấy từ file login.html
        password = request.POST.get('password')  # lấy từ file login.html
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'home.html', context)
        else:
            messages.info(request, 'Tài khoản hoặc mật khẩu không chính xác!')
    return render(request, 'login.html')

def logoutPage(request):
    context = {'user_not_login': "hidden",
               'user_login': "show"}
    logout(request)
    return render(request, 'home.html', context)

def detail(request):
    context = {'user_not_login': "hidden",
               'user_login': "show"}
    return render(request, 'detail.html', context)