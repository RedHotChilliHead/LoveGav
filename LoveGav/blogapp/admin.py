from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Post - постов
    """
    ordering = ('pk',)  # сортировка
    list_display = "pk", "description", "data", "author"
    list_display_links = "pk", "description", "data", "author"
    search_fields = ("description", "data", "author")

    def description_short(self, obj: Post) -> str:  # вывод короткого описания
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Comment - комментариев к посту
    """
    ordering = ('pk',)  # сортировка
    list_display = "pk", "post", "body", "data", "author"
    list_display_links = "pk", "post", "body", "data", "author"
    search_fields = ("post", "body", "data", "author")

    def description_short(self, obj: Comment) -> str:  # вывод короткого описания
        if len(obj.body) < 48:
            return obj.body
        return obj.body[:48] + "..."
