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