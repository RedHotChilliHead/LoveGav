from django.contrib import admin
from .models import Playground

@admin.register(Playground)
class PlaygroundAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "town", "address", "description"
    list_display_links = "pk", "town", "address", "description"
    search_fields = ('town', 'address', 'description')
    def description_short(self, obj: Playground) -> str:  # вывод короткого описания
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."
