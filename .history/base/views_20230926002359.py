from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from base.forms import PostForm
from .models import *
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
    post = Posts.objects.all()
    user = get_common_context(request)
    # Truyền danh sách bài viết vào template
    context = {'user': user, 'posts': post}
    return render(request, 'home.html', context)


def classes(request):
    # Truy vấn tất cả các bài viết từ cơ sở dữ liệu
    post = Posts.objects.all()
    user = get_common_context(request)
    # Truyền danh sách bài viết vào template
    context = {'user': user, 'posts': post}
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
    # Cập nhật cơ sở dữ liệu trước khi đăng xuất
    deleted_posts = request.session.get('deleted_posts', [])
    Posts.objects.filter(id__in=deleted_posts).update(is_deleted=True)

    # Xóa 'deleted_posts' khỏi session để tránh tác động đến phiên làm việc sau
    if 'deleted_posts' in request.session:
        del request.session['deleted_posts']

    logout(request)
    # return render(request, 'home.html', context)
    return redirect('home')


def detailPage(request, pk):
    context = get_common_context(request)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'detail.html', context)


def dashboard(request):
    return render(request, 'admin/dashboard.html')


@login_required
def postManage(request):
    user_not_admin = "none"
    if request.user.is_superuser:
        user_not_admin = "block"
        # Nếu người dùng là admin, lấy tất cả bài viết
        posts = Posts.objects.all()
    else:
        # Nếu người dùng không phải là admin, lấy các bài viết của người dùng hiện tại
        posts = Posts.objects.filter(author=request.user)
    context = {'user_not_admin': user_not_admin, 'posts': posts}
    return render(request, 'admin/post-manage.html', context)


def addPost(request, post_id=None):
    user_new, user_update = "none", "block"
    if post_id:
        # lấy ra đối tượng Posts dựa trên post_id hoặc trả về một lỗi 404 nếu không tìm thấy.
        post = get_object_or_404(Posts, id=post_id)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                if 'image' in request.FILES:  # Kiểm tra xem có tải lên hình ảnh mới không
                    post.image = request.FILES['image']
                post.author = request.user
                post.save()
                return redirect(reverse('postManage'))
        else:
            form = PostForm(instance=post)
    else:
        user_new, user_update = "block", "none"
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                # Tạo đối tượng post nhưng chưa lưu vào database
                post = form.save(commit=False)
                post.author = request.user  # Gán người dùng hiện tại làm tác giả
                post.save()  # Lưu bài viết vào cơ sở dữ liệu
            # Sử dụng reverse() với tên định tuyến chính xác 'postManage'
                post_manage_url = reverse('postManage')
            # Sử dụng redirect() để thực hiện chuyển hướng
                return redirect(post_manage_url)
        else:
            form = PostForm()
    content = {'form': form, 'post': post if post_id else None,
               'post_id': post_id, 'user_new': user_new, 'user_update': user_update}
    return render(request, 'admin/add-post.html', content)
