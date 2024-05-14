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


def answers_photo_path(instance: "Answer", filename: str) -> str:
    return 'answers/{author}/{filename}'.format(
        author=instance.author,
        filename=filename,
    )


class Playground(models.Model):
    """
    Модель площадки для выгула собак
    """
    class Meta:
        ordering = ["town"]
    town = models.CharField(max_length=100, blank=False)
    address = models.TextField(max_length=150, blank=False)
    description = models.CharField(max_length=200, null=False, blank=True)
    photo = models.ImageField(null=True, upload_to=playgrounds_photo_path)

    def __str__(self) -> str:
        return f"Playground({self.pk})"


class Question(models.Model):
    """
    Модель вопроса пользователя
    """
    head = models.CharField(max_length=100, blank=False)
    body = models.TextField(max_length=500, blank=False)
    data = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, upload_to=questions_photo_path, blank=True)
    # answers = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)  # связь с таблицей ответов
    def __str__(self) -> str:
        return f"({self.head})"


class Answer(models.Model):
    """
    Модель ответа на вопрос пользователя
    """
    body = models.TextField(max_length=500, blank=False)
    data = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, upload_to=answers_photo_path, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)  # связь с таблицей вопросов
    def __str__(self) -> str:
        return f"({self.body[:15]}...)"

