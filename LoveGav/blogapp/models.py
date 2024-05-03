from django.contrib.auth.models import User
from django.db import models

def posts_photo_path(instance: "Post", filename: str) -> str:
    return 'posts/{author}/{filename}'.format(
        author=instance.author,
        filename=filename,
    )

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True)
    data = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True, upload_to=posts_photo_path)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=150, blank=True)
    data = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

