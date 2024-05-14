from django.contrib import admin
from .models import Pet, Profile, Mood, Heat, Treatment


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "name", "breed", "owner", "sex"
    list_display_links = "pk", "name", "breed", "owner", "sex"
    search_fields = ("name", "breed", "owner", "sex")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "user", "bio", "email", "birth"
    list_display_links = "pk", "user", "bio", "email", "birth"
    search_fields = ("user", "bio", "email", "birth")

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "pet", "mood_day", "data"
    list_display_links = "pk", "pet", "mood_day", "data"
    search_fields = ("pet", "mood_day", "data")

@admin.register(Heat)
class HeatAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "pet", "soreness", "data"
    list_display_links = "pk", "pet", "soreness", "data"
    search_fields = ("pet", "soreness", "data")

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    ordering = ('pk',)  # сортировка
    list_display = "pk", "pet", "name", "data", "data_next"
    list_display_links = "pet", "name", "data", "data_next"
    search_fields = ("pet", "name", "data", "data_next")
