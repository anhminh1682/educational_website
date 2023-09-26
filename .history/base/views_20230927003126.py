from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.urls import reverse
from base.forms import PostForm
from .models import *
import json
import base64
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def get_common_context(request):
    context = {'user_not_login': "none", 'user_login': "block"}
    if request.user.is_authenticated:
        context = {'user_not_login': "block", 'user_login': "none"}
    return context


def home(request):
    # Truy vấn tất cả các bài viết từ cơ sở dữ liệu
    posts = Posts.objects.filter(is_deleted=False)
    user = get_common_context(request)
    # Truyền danh sách bài viết vào template
    context = {'user': user, 'posts': posts}
    return render(request, 'home.html', context)


def classes(request):
    # Truy vấn tất cả các bài viết từ cơ sở dữ liệu
    posts = Posts.objects.filter(is_deleted=False)
    user = get_common_context(request)
    print(posts)
    # Truyền danh sách bài viết vào template
    context = {'user': user, 'posts': posts}
    return render(request, 'classes.html', context)


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
    # Xóa các bài viết có trường is_deleted=True
    Posts.objects.filter(is_deleted=True).delete()

    # Không cần lưu trữ danh sách 'deleted_posts' trong session nữa
    if 'deleted_posts' in request.session:
        del request.session['deleted_posts']

    logout(request)
    return redirect('home')

@login_required
def detailPage(request, post_id):    
    user = get_common_context(request)
    # Lấy post dựa trên post_id
    post = get_object_or_404(Posts, id=post_id, is_deleted=False)
    # Lấy tên của người viết
    author_name = post.author.username 
    paragraphs = post.content.split('\n')
    context = {'user': user, 'post': post, 'paragraphs': paragraphs, 'writer':author_name}
    return render(request, 'detail.html', context)

@login_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')


def deletePost(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        try:
            post = Posts.objects.get(id=post_id)
            post.is_deleted = True
            post.save()
            return JsonResponse({"success": True}, status=200)
        except Posts.DoesNotExist:
            return JsonResponse({"success": False, "error": "Bài viết không tồn tại"}, status=404)
    return JsonResponse({"success": False, "error": "Phương thức không được hỗ trợ"}, status=405)


# `@login_required` is a decorator in Django that is used to restrict access to a view function to
# only authenticated users. It checks if the user is authenticated, and if not, it redirects the user
# to the login page. This decorator is commonly used to protect views that require authentication,
# such as user profiles or dashboard pages.
@login_required
def postManage(request):
    user_not_admin = "none"
    if request.user.is_superuser:
        user_not_admin = "block"
        # Nếu người dùng là admin, lấy tất cả bài viết
        posts = Posts.objects.filter(is_deleted=False)
    else:
        # Nếu người dùng không phải là admin, lấy các bài viết của người dùng hiện tại
        posts = Posts.objects.filter(author=request.user, is_deleted=False)
    context = {'user_not_admin': user_not_admin, 'posts': posts}
    return render(request, 'admin/post-manage.html', context)

def handle_post_creation(request, form):
    """
    Xử lý việc tạo mới một bài viết.

    Args:
    - request: Đối tượng HttpRequest từ Django.
    - form: Đối tượng form chứa dữ liệu từ client.

    Returns:
    - HttpResponse: Chuyển hướng tới trang quản lý bài viết sau khi tạo thành công.
    """
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect(reverse('postManage'))


def handle_post_update(request, post, form):
    """
    Xử lý việc cập nhật một bài viết.

    Args:
    - request: Đối tượng HttpRequest từ Django.
    - post: Đối tượng bài viết cần cập nhật.
    - form: Đối tượng form chứa dữ liệu từ client.

    Returns:
    - HttpResponse: Chuyển hướng tới trang quản lý bài viết sau khi cập nhật thành công.
    """
    post = form.save(commit=False)
    if 'image' in request.FILES:
        post.image = request.FILES['image']
    post.author = request.user
    post.save()
    return redirect(reverse('postManage'))


def addPost(request, post_id=None):
    """
    Xử lý việc thêm hoặc cập nhật bài viết dựa trên việc có post_id hay không.

    Args:
    - request: Đối tượng HttpRequest từ Django.
    - post_id (optional): ID của bài viết cần cập nhật. Nếu không có thì tạo mới.

    Returns:
    - HttpResponse: Render template tương ứng hoặc chuyển hướng tới trang quản lý bài viết.
    """
    user_new, user_update = "none", "block"
    is_required = not bool(post_id)

    if post_id:
        post = get_object_or_404(Posts, id=post_id)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                return handle_post_update(request, post, form)
        else:
            form = PostForm(instance=post)
    else:
        user_new, user_update = "block", "none"
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                return handle_post_creation(request, form)
        else:
            form = PostForm()

    content = {
        'form': form,
        'post': post if post_id else None,
        'post_id': post_id,
        'user_new': user_new,
        'user_update': user_update,
        'is_required': is_required
    }

    return render(request, 'admin/add-post.html', content)

def error(request):
    return render(request, 'error/error.html')