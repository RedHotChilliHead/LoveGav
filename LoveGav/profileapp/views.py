from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from profileapp.models import Profile, Pet


class RegisterView(CreateView):  # форма регистрации пользователя
    """
    Создать пользователя
    """
    form_class = UserCreationForm  # создать пользователя такого типа
    template_name = 'profileapp/register.html'  # указание шаблона
    # success_url = reverse_lazy("profileapp:user-details", kwargs={'username': })  # редирект на инфу о пользователе

    def form_valid(self, form):  # переопределение метода, чтоб после создания пользователя проходила аутентификация
        response = super().form_valid(form)  # подготовка ответа, пользователь сохранен, публикация формы
        Profile.objects.create(user=self.object)  # добавление пользователю профиль
        username = form.cleaned_data.get('username')  # получение из формы username
        password = form.cleaned_data.get('password1')  # получение из формы password
        user = authenticate(self.request, username=username, password=password)  # получили аутентифицированного пользователя
        login(request=self.request, user=user)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:user-details", kwargs={'username': self.request.user.username})

def logout_view(request:HttpRequest):
    """
    Выход из аккаунта
    """
    logout(request)
    return redirect(reverse("profileapp:login")) #revers работает только внутри view функций


class UpdateMeView(LoginRequiredMixin, UpdateView):
    """
    Редактировать профиль
    """
    model = Profile
    fields = "bio", "email", "birth", "avatar"
    template_name = 'profileapp/update-me.html'

    def get_object(self,
                   queryset=None):  # для передачи доп. параметра as_view(), get_object отвечает за извлечение записи
        user = get_object_or_404(User, username=self.request.user.username)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    def get_success_url(self):
        return reverse("profileapp:user-details", kwargs={'username': self.request.user.username})

class UserDetaislView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    """
    Просмотр профиля
    """
    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff:
            return True
        elif self.request.user.pk == owner.id:
            return True
        else:
            return False

    model = Profile
    template_name = 'profileapp/user_profile.html'

    def get_object(self, queryset=None): #получить или создать экземпляр профиля на основе имени пользователя из URL
        user = get_object_or_404(User, username=self.kwargs['username'])
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    def get_context_data(self, **kwargs): #добавить объект user в контекст, чтобы он был доступен в шаблоне
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user #поле user-владельца записи
        context['pet'] = self.object.user.pet
        return context

class HellowView(View):
    """
    Домашняя страница-заглушка
    """
    def get(self, request:HttpRequest) -> HttpResponse:
        context = {
            "user": self.request.user,
        }
        return render(request, 'profileapp/hello.html', context=context)

class RegisterPetView(CreateView):
    """
    Создание странички питомца
    """
    model = Pet
    fields = "name", "sex", "specie", "breed", "color", "birth", "chip", "tatoo", "date_tatoo"
    template_name = 'profileapp/pet_form.html'

    def form_valid(self, form):  # переопределение метода, чтоб после создания пользователя проходила аутентификация
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:user-details", kwargs={'username': self.request.user.username})

