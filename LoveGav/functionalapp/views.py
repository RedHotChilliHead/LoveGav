import datetime
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import Calculator, AnswerForm
from django.views import View
from profileapp.models import Pet
from functionalapp.models import Playground, Question, Answer
from django.http import HttpRequest, HttpResponse


class HelloView(View):
    """
    Домашняя страница-заглушка
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        now = datetime.date.today()
        notifications = []
        if request.user.is_authenticated and request.user.pet_set:
            for pet in request.user.pet_set.all():
                for treatment in pet.treatment_set.all():
                    if treatment.data_next - now < timedelta(7):
                        notifications.append(f"Warning: {treatment.data_next}, it's time to apply {treatment.name}")
        context = {
            "notifications": notifications,
        }
        return render(request, 'functionalapp/hello.html', context=context)


class СalorieСalculatorView(LoginRequiredMixin, View):
    """
    Калькулятор калорий
    """

    def get(self, request, *args, **kwargs):
        form = Calculator()
        context = {
            "pets": Pet.objects.filter(owner__username=self.request.user.username),
            "form": form,
        }
        return render(request, 'functionalapp/calories.html', context=context)

    def post(self, request, *args, **kwargs):
        form = Calculator(request.POST)
        context = {
            "pets": Pet.objects.filter(owner__username=self.request.user.username),
            "form": form,
        }
        if form.is_valid():
            weight = form.cleaned_data['weight']
            if weight < 2:
                result = 2 * (70 * weight ** 0.75)
            else:
                result = 2 * (30 * weight + 70)
            kkk = [form.cleaned_data['k' + str(i)] for i in range(1, 11)]
            kkk_dict = {'k1': 1.2,
                        'k2': 3,
                        'k3': 0.8,
                        'k4': 2.4,
                        'k5': 2,
                        'k6': 1.6,
                        'k7': 1.2,
                        'k8': 1.6,
                        'k9': 1.6,
                        'k10': 1.2}
            count = 1
            for k in kkk:
                if k == True:
                    result *= kkk_dict['k' + str(count)]
                count += 1
            context['calories_per_day'] = result
            if form.cleaned_data['calorie_content']:
                calorie_content = form.cleaned_data['calorie_content']
                one_calorie = 1000 / calorie_content
                context['grams'] = result * one_calorie
        return render(request, 'functionalapp/calories.html', context=context)


class DogPlaygroundsView(ListView):
    """
    Отображение списка собачьих площадок
    """
    model = Playground
    template_name = "functionalapp/playgrounds.html"
    paginate_by = 100


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    Задать вопрос
    """
    model = Question
    fields = "head", "body", "photo"
    template_name = 'functionalapp/question_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("functionalapp:question-details", kwargs={'pk': self.object.pk})


class QuestionListView(ListView):
    """
    Отобразить список вопросов
    """
    model = Question
    template_name = 'functionalapp/question_list.html'
    paginate = 30

class QuestionDetailsView(View):
    """
    Просмотреть страничку вопроса и ответы на него
    """

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form = AnswerForm()
        context = {
            "question": question,
            "form": form,
            'permission': self.request.user.is_staff or self.request.user.pk == question.author.id,
        }

        return render(request, 'functionalapp/question_details.html', context=context)

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form = AnswerForm(request.POST, request.FILES)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('functionalapp:question-list')
        else:
            context = {
                'question': question,
                'form': form,
                'permission': self.request.user.is_staff or self.request.user.pk == question.author.id
            }
            return render(request, 'functionalapp/question_details.html', context=context)

class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Редактировать вопрос
    """

    def test_func(self):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        if self.request.user.is_staff or self.request.user.pk == question.author.id:
            return True

    model = Question
    fields = "head", "body", "photo"
    template_name = 'functionalapp/question_update.html'

    def get_success_url(self):
        return reverse_lazy("functionalapp:question-details", kwargs={'pk': self.object.pk})


class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить вопрос
    """

    def test_func(self):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        if self.request.user.is_staff or self.request.user.pk == question.author.id:
            return True

    model = Question
    template_name = "functionalapp/question_confirm_delete.html"
    success_url = reverse_lazy("functionalapp:question-list")

class AnswerDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Удалить ответ
    """

    def test_func(self):
        answer = get_object_or_404(Answer, pk=self.kwargs['pk'])
        if self.request.user.is_staff or self.request.user.pk == answer.author.id:
            return True

    model = Answer
    template_name = "functionalapp/answer_confirm_delete.html"

    def get_success_url(self):
        answer = get_object_or_404(Answer, pk=self.kwargs['pk'])
        return reverse_lazy("functionalapp:question-details", kwargs={'pk': answer.question.pk})