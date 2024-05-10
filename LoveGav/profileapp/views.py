from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from profileapp.models import Profile, Pet, Mood, Heat, Treatment
from fpdf import FPDF

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
    success_url = reverse_lazy("functionalapp:hello")
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["mood"] = Mood.objects.filter(pet=self.object).latest('data')
        except Mood.DoesNotExist:
            context["mood"] = None

        try:
            context["heat"] = Heat.objects.filter(pet=self.object).latest('data')
        except Heat.DoesNotExist:
            context["heat"] = None

        try:
            context["treatment"] = Treatment.objects.filter(pet=self.object).latest('data')
        except Treatment.DoesNotExist:
            context["treatment"] = None

        return context


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
        return reverse("profileapp:user-details", kwargs={'username': self.kwargs['username']})


class CreateMoodView(UserPassesTestMixin, CreateView):
    """
    Создание записи о настроении
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Mood
    fields = "mood_day", "data"
    template_name = 'profileapp/mood.html'

    def form_valid(self, form):
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:pet-details", kwargs=self.kwargs)


class DeleteMoodView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить запись о настроении
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Mood
    template_name = "profileapp/mood_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("profileapp:pet-details",
                            kwargs={'username': self.kwargs['username'], 'pk': self.object.pet.pk})


class CreateHeatView(UserPassesTestMixin, CreateView):
    """
    Создание записи о течке
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Heat
    fields = "soreness", "data"
    template_name = 'profileapp/heat.html'

    def form_valid(self, form):
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:pet-details", kwargs=self.kwargs)


class DeleteHeatView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить запись о течке
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Heat
    template_name = "profileapp/heat_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("profileapp:pet-details",
                            kwargs={'username': self.kwargs['username'], 'pk': self.object.pet.pk})


class CreateTreatmentView(UserPassesTestMixin, CreateView):
    """
    Создание записи о лечении, обработках и вакцинировании
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Treatment
    fields = "name", "data", "data_next"
    template_name = 'profileapp/treatment.html'

    def form_valid(self, form):
        form.instance.pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("profileapp:pet-details", kwargs=self.kwargs)


class DeleteTreatmentView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить запись о лечении, обработках и вакцинировании
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Treatment
    template_name = "profileapp/treatment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("profileapp:pet-details",
                            kwargs={'username': self.kwargs['username'], 'pk': self.object.pet.pk})


class DairyDetaislView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    """
    Просмотр подробной информации об обработках, течках и вакцинировании питомца
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    model = Pet
    template_name = 'profileapp/dairy.html'
    context_object_name = 'pet'


class DairyPetDataExportView(UserPassesTestMixin, LoginRequiredMixin, View):
    """
    Представление экспорта дневника конкретного питомца в pdf
    """

    def test_func(self):
        owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff or self.request.user.pk == owner.id:
            return True

    def get(self, request: HttpRequest, username, pk):
        pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        try:
            moods = Mood.objects.filter(pet=pet)
        except Mood.DoesNotExist:
            moods = None
        try:
            heats = Heat.objects.filter(pet=pet)
        except Heat.DoesNotExist:
            heats = None
        try:
            treatments = Treatment.objects.filter(pet=pet)
        except Heat.DoesNotExist:
            treatments = None

        pdf = FPDF()  # (orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("times", size=18)

        pdf.image("profileapp/static/Lovegav.png", x=50, y=None, h=20)
        pdf.cell(200, 10, txt="", ln=1, align="L")
        text = str(pet.name) + "`s dairy "
        pdf.cell(200, 10, txt=text, ln=1, align="C")
        pdf.cell(200, 10, txt="", ln=1, align="L")

        if moods:
            pdf.set_font("times", size=18)
            pdf.cell(200, 10, txt="Moods", ln=1, align="L")
            pdf.set_font("times", size=14)
            for mood in moods:
                text = str(mood.mood_day) + " at " + str(mood.data)
                pdf.cell(200, 10, txt=text, ln=1, align="L")
        pdf.cell(200, 10, txt="", ln=1, align="L")

        if heats:
            pdf.set_font("times", size=18)
            pdf.cell(200, 10, txt="Heats", ln=1, align="L")
            pdf.set_font("times", size=14)
            for heat in heats:
                text = str(heat.soreness) + " at " + str(heat.data)
                pdf.cell(200, 10, txt=text, ln=1, align="L")
        pdf.cell(200, 10, txt="", ln=1, align="L")

        if treatments:
            pdf.set_font("times", size=18)
            pdf.cell(200, 10, txt="Treatments", ln=1, align="L")
            pdf.set_font("times", size=14)
            for treatment in treatments:
                text = str(treatment.name) + " at " + str(treatment.data) + " and next data: " + str(
                    treatment.data_next)
                pdf.cell(200, 10, txt=text, ln=1, align="L")
        pdf.cell(200, 10, txt="", ln=1, align="L")

        pdf.output("dairy_demo.pdf")

        return redirect(reverse("profileapp:dairy-pet-details", kwargs=self.kwargs))
