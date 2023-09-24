from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def get_common_context(request):
    context = {'user_not_login': "hidden", 'user_login': "show"}
    if request.user.is_authenticated:
        context = {'user_not_login': "show", 'user_login': "hidden"}
    return context


def home(request):
    context = get_common_context(request)
    return render(request, 'home.html', context)


def classes(request):
    return render(request, 'classes.html')


def loginPage(request):
    context = get_common_context(request)
    next_url = request.GET.get('next', '')
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
            messages.info(request, 'Tài khoản hoặc mật khẩu không chính xác!')
    return render(request, 'login.html')


def logoutPage(request):
    context = get_common_context(request)
    logout(request)
    # return render(request, 'home.html', context)
    return redirect('home')


def detailPage(request):
    context = get_common_context(request)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'detail.html', context)
