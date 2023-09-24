from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html')

def classes(request):
    return render(request, 'classes.html')

def login(request):
    return render(request, 'login.html')

def detail(request):
    return render(request, 'detail.html')

def dashboard(request):
    return render(request, 'admin/dashboard.html')

def postManage(request):
    return render(request, 'admin/post-manage.html')

def addPost(request):
    return render(request, 'admin/add-post.html')