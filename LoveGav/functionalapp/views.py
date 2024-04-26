from django.shortcuts import render
from django.views.generic import ListView

from profileapp.forms import Calculator
from django.views import View
from django.contrib.auth.models import User
from profileapp.models import Pet
from functionalapp.models import Playground
from django.http import HttpRequest, HttpResponse

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
                    result *= kkk_dict['k'+str(count)]
                count += 1
            context['calories_per_day'] = result
            if form.cleaned_data['calorie_content']:
                calorie_content = form.cleaned_data['calorie_content']
                one_calorie = 1000/calorie_content
                context['grams'] = result * one_calorie
        return render(request, 'functionalapp/calories.html', context=context)

class DogPlaygroundsView(ListView):
    model = Playground
    template_name = "functionalapp/playgrounds.html"
    paginate_by = 100
