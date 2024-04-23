from django.urls import path
from django.contrib.auth.views import LoginView

from .views import RegisterView, logout_view, UpdateMeView, UserDetaislView, HellowView
from .views import RegisterPetView

app_name = "profileapp"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register_pet/', RegisterPetView.as_view(), name='register-pet'),
    path('login/',
             LoginView.as_view(template_name='profileapp/login.html', redirect_authenticated_user=True),
             name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/<str:username>/update/', UpdateMeView.as_view(), name='update-me'),
    path('user/<str:username>/', UserDetaislView.as_view(), name='user-details'),
    path('hello/', HellowView.as_view(), name='hello'),
]