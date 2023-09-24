from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     # path('home/', views.home, name="home"),
     path('classes/', views.classes, name="classes"),
     path('login/', views.login, name="login"),
     path('detail/', views.detail, name="detail"),
     path('dashboard/', views.dashboard, name="dashboard"),
     path('post-manage/', views.postManage, name="postManage"),
     path('add-post/', views.addPost, name="addPost"),
]