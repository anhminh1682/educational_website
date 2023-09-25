from django.db import models

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    title = models.CharField(max_length=200, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    content = models.TextField()

    def __str__(self):
        return self.title
