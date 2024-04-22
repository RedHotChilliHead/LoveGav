from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str: #instance-то, над чем производят действие
    return 'users/user{pk}/images/{filename}'.format(
        pk=instance.user.pk,
        filename=filename,
    )
class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE) #если user удален, удалить всю модель. благодаря этой связи можно обращаться по .profile
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(null=True, upload_to=profile_avatar_directory_path)
