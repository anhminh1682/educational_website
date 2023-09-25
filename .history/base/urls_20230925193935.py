from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     path('classes/', views.classes, name="classes"),
     path('login/', views.loginPage, name="login"),
     path('logout/', views.logoutPage, name="logout"),
     path('detail/', views.detailPage, name="detail"),
     path('dashboard/', views.dashboard, name="dashboard"),
     path('post-manage/', views.postManage, name="postManage"),
     path('add-post/', views.addPost, name="addPost"),
     path('update-post/, views.updatePost, name=')
]