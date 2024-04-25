from django.urls import path
from .views import HelloView
from .views import СalorieСalculatorView

app_name = "functionalapp"

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('<str:username>/calculator/', СalorieСalculatorView.as_view(), name='calculator'),
]
