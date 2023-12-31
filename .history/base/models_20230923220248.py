from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Lưu ý: Trong thực tế, bạn nên sử dụng một hàm băm (hashing) cho mật khẩu.

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title