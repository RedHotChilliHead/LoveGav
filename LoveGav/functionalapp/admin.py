from django.contrib import admin
from .models import Playground, Question, Answer


@admin.register(Playground)
class PlaygroundAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Playground - собачьих площадок
    """
    ordering = ('pk',)  # сортировка
    list_display = "pk", "town", "address", "description"
    list_display_links = "pk", "town", "address", "description"
    search_fields = ('town', 'address', 'description')
    def description_short(self, obj: Playground) -> str:  # вывод короткого описания
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Question - вопросов пользователей
    """
    ordering = ('pk',)  # сортировка
    list_display = "pk", "head", "body", "data", "author"
    list_display_links = "pk", "head", "body", "data", "author"
    search_fields = ("head", "body", "data", "author")
    def description_short(self, obj: Question) -> str:  # вывод короткого описания
        if len(obj.body) < 48:
            return obj.body
        return obj.body[:48] + "..."

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Answer - ответов на вопросы пользователей
    """
    ordering = ('pk',)  # сортировка
    list_display = "pk", "question", "body", "data", "author"
    list_display_links = "pk", "question", "body", "data", "author"
    search_fields = ("question", "body", "data", "author")
    def description_short(self, obj: Answer) -> str:  # вывод короткого описания
        if len(obj.body) < 48:
            return obj.body
        return obj.body[:48] + "..."