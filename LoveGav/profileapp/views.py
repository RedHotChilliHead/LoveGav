from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from profileapp.models import Profile, Pet


class RegisterView(CreateView):  # форма регистрации пользователя
    """
    Создать пользователя
    """
    form_class = UserCreationForm  # создать пользователя такого типа
    template_name = 'profileapp/register.html'  # указание шаблона

    def form_valid(self, form):  # переопределение метода, чтоб после создания пользователя проходила аутентификация
        response = super().form_valid(form)  # подготовка ответа, пользователь сохранен, публикация формы
        Profile.objects.create(user=self.object)  # добавление пользователю профиль
        username = form.cleaned_data.get('username')  # получение из формы username
        password = form.cleaned_data.get('password1')  # получение из формы password
        user = authenticate(self.request, username=username,
                            password=password)  # получили аутентифицированного пользователя
        login(request=self.request, user=user)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:user-details", kwargs={'username': self.request.user.username})


class DeleteUserView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить профиль владельца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = User
    success_url = ("profileapp:hello")
    template_name = "profileapp/user_confirm_delete.html"


def logout_view(request: HttpRequest):
    """
    Выход из аккаунта владельца
    """
    logout(request)
    return redirect(reverse("profileapp:login"))  # revers работает только внутри view функций


class UpdateMeView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Редактировать профиль владельца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

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
    Просмотр приватного профиля владельца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Profile
    template_name = 'profileapp/user_profile.html'

    def get_object(self, queryset=None):  # получить или создать экземпляр профиля на основе имени пользователя из URL
        user = get_object_or_404(User, username=self.kwargs['username'])
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    def get_context_data(self, **kwargs):  # добавить объект user в контекст, чтобы он был доступен в шаблоне
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user  # поле user-владельца записи
        context['pets'] = self.object.user.pet_set.all()
        return context

class RegisterPetView(UserPassesTestMixin, CreateView):
    """
    Создание странички питомца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Pet
    fields = "name", "sex", "specie", "breed", "color", "birth", "chip", "tatoo", "date_tatoo", "weight"
    template_name = 'profileapp/pet_form.html'

    def form_valid(self, form):  # переопределение метода, чтоб после создания пользователя проходила аутентификация
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:user-details", kwargs={'username': self.request.user.username})


class PetDetaislView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    """
    Просмотр профиля питомца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Pet
    template_name = 'profileapp/pet_profile.html'
    context_object_name = 'pet'


class UpdatePetView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Редактировать профиль питомца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Pet
    fields = "specie", "breed", "color", "birth", "chip", "tatoo", "date_tatoo", "passport", "avatar", "weight"
    template_name = 'profileapp/update-pet.html'

    def get_success_url(self):
        return reverse("profileapp:pet-details", kwargs={'username': self.kwargs['username'], 'pk': self.kwargs['pk']})


class DeletePetView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить профиль питомца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Pet
    template_name = "profileapp/pet_confirm_delete.html"

    def get_success_url(self):
        return reverse("profileapp:pet-details", kwargs={'username': self.kwargs['username'], 'pk': self.kwargs['pk']})