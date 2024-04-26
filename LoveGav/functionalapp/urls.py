from django.urls import path
from .views import HelloView
from .views import СalorieСalculatorView, DogPlaygroundsView

app_name = "functionalapp"

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('<str:username>/calculator/', СalorieСalculatorView.as_view(), name='calculator'),
    path('playgrounds/', DogPlaygroundsView.as_view(), name="playground-list"),
]
