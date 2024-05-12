from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField


def profile_avatar_directory_path(instance: "Profile",
                                  filename: str) -> str:  # instance-то, над чем производят действие
    return 'users/user{pk}/images/{filename}'.format(
        pk=instance.user.pk,
        filename=filename,
    )


def pet_files_path(instance: "Pet", filename: str) -> str:
    return 'users/user{pk}/pet_files/{filename}'.format(
        pk=instance.owner.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = OneToOneField(User,
                         on_delete=models.CASCADE, blank=True,
                         null=True)  # если user удален, удалить всю модель. благодаря этой связи можно обращаться по .profile
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(null=True, upload_to=profile_avatar_directory_path)


class Pet(models.Model):
    class Meta:
        ordering = ["name"]

    SEX_CHOICES = {
        'M': "Male",
        'F': "Famale",
    }

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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
    passport = models.FileField(null=True, upload_to=pet_files_path, blank=True)
    avatar = models.ImageField(null=True, upload_to=pet_files_path, blank=True)
    weight = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return f"({self.name})"


class Mood(models.Model):
    MOOD_CHOICES = {
        'slug': "sluggish",
        'rest': "restless",
        'aggr': "aggressive",
        'norm': "normal",
        'play': "playful",
        'exc': "excellent",
    }

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    mood_day = models.CharField(
        max_length=4,
        choices=MOOD_CHOICES,
    )
    data = models.DateField(blank=False, null=False)


class Heat(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    soreness = models.CharField(max_length=50, blank=True, null=True)
    data = models.DateField(blank=False, null=False)


class Treatment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False, null=False)
    data = models.DateField(blank=False, null=False)
    data_next = models.DateField(blank=False, null=False)
