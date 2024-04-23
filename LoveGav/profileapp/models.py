from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str: #instance-то, над чем производят действие
    return 'users/user{pk}/images/{filename}'.format(
        pk=instance.user.pk,
        filename=filename,
    )

def pet_passport_path(instance: "Pet", filename: str) -> str:
    return 'users/user{pk}/pet_files/{filename}'.format(
        pk=instance.owner.pk,
        filename=filename,
    )
class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE) #если user удален, удалить всю модель. благодаря этой связи можно обращаться по .profile
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(null=True, upload_to=profile_avatar_directory_path)

class Pet(models.Model):
    SEX_CHOICES = {
        'M': "Male",
        'F': "Famale",
    }

    owner = OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
    )
    specie = models.CharField(max_length=20, blank=True, null=True)
    breed = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    chip = models.BooleanField(blank=True, null=True)
    tatoo = models.TextField(max_length=20, blank=True)
    date_tatoo = models.DateField(blank=True, null=True)
    passport = models.FileField(null=True, upload_to=pet_passport_path)

