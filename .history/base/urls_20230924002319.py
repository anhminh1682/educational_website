from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     path('home/', views.home, name="home"),
     path('classes/', views.classes, name="classes"),
     path('login/', views.loginPage, name="login"),
     path('logout/', views.loginPage, name="login"),
     path('detail/', views.detail, name="detail"),
]