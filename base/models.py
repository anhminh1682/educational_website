from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title