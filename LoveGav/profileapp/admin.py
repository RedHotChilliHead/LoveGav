from django.contrib import admin
from .models import Pet
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "name", "breed", "owner", "sex"
    list_display_links = "pk", "name", "breed", "owner", "sex"
    search_fields = ("name", "breed", "owner", "sex")
