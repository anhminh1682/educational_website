from django.shortcuts import redirect, render
from django.urls import reverse
from base.forms import PostForm
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


def dashboard(request):
    return render(request, 'admin/dashboard.html')


def postManage(request):
    return render(request, 'admin/post-manage.html')


def addPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Lưu bài viết vào cơ sở dữ liệu
            # Chuyển hướng sau khi lưu thành công
            # Sử dụng reverse() để xác định URL của post-manage
            post_manage_url = reverse('post-manage') 
            # Sử dụng redirect() để thực hiện chuyển hướng
            return redirect(post_manage_url)
    else:
        form = PostForm()
    return render(request, 'admin/add-post.html', {'form': form})
