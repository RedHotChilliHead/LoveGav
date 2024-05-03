from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import Calculator, AnswerForm
from django.views import View
from django.contrib.auth.models import User
from profileapp.models import Pet
from functionalapp.models import Playground, Question, Answer
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


class HelloView(View):
    """
    Домашняя страница-заглушка
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "user": self.request.user,
        }
        return render(request, 'functionalapp/hello.html', context=context)


class СalorieСalculatorView(View):
    """
    Калькулятор каллорий
    """

    def get(self, request, *args, **kwargs):
        form = Calculator()
        arg_username = self.kwargs['username']
        context = {
            "pets": Pet.objects.filter(owner__username=arg_username),
            "user": User.objects.get(username=arg_username),
            "form": form,
        }
        return render(request, 'functionalapp/calories.html', context=context)

    def post(self, request, *args, **kwargs):
        form = Calculator(request.POST)
        arg_username = self.kwargs['username']
        context = {
            "pets": Pet.objects.filter(owner__username=arg_username),
            "user": User.objects.get(username=arg_username),
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
        answers = Answer.objects.filter(question=question)
        context = {
            "question": question,
            "form": form,
            "answers": answers,
            'permission': self.request.user.is_staff or self.request.user.pk == question.author.id
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
            answers = Answer.objects.filter(question=question)
            context = {
                'question': question,
                'form': form,
                'answers': answers,
                'permission': self.request.user.is_staff or self.request.user.pk == question.author.id
            }
            return render(request, 'functionalapp/question_details.html', context=context)

class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Редактировать вопрос
    """

    def test_func(self):
        # owner = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.is_staff:
            return True
        elif self.request.user.pk == self.object.author.id:
            return True
        else:
            return False

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
        if self.request.user.is_staff:
            return True
        elif self.request.user.pk == self.object.author.id:
            return True
        else:
            return False

    model = Question
    template_name = "functionalapp/question_confirm_delete.html"
    success_url = reverse_lazy("functionalapp:question-list")
