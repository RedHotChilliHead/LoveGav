from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField


def playgrounds_photo_path(instance: "Playground", filename: str) -> str:
    return 'playgrounds/{town}/{filename}'.format(
        town=instance.town,
        filename=filename,
    )


def questions_photo_path(instance: "Question", filename: str) -> str:
    return 'questions/{author}/{filename}'.format(
        author=instance.author,
        filename=filename,
    )


class Playground(models.Model):
    town = models.CharField(max_length=100, blank=False)
    address = models.TextField(max_length=150, blank=False)
    description = models.CharField(max_length=200, null=False, blank=True)
    photo = models.ImageField(null=True, upload_to=playgrounds_photo_path)

    def __str__(self) -> str:
        return f"Playground({self.pk})"


class Answer(models.Model):
    body = models.TextField(max_length=500, blank=False)
    data = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, upload_to=questions_photo_path)


class Question(models.Model):
    head = models.CharField(max_length=100, blank=False)
    body = models.TextField(max_length=500, blank=False)
    data = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, upload_to=questions_photo_path, blank=True)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)  # связь с таблицей ответов
