from django.urls import path
from django.contrib.auth.views import LoginView

from .views import RegisterView, logout_view, UpdateMeView, UserDetaislView, HellowView
from .views import RegisterPetView, PetDetaislView, UpdatePetView, DeletePetView

app_name = "profileapp"

urlpatterns = [
    path('hello/', HellowView.as_view(), name='hello'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/',
         LoginView.as_view(template_name='profileapp/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', logout_view, name='logout'),

    path('<str:username>/', UserDetaislView.as_view(), name='user-details'),
    path('<str:username>/update/', UpdateMeView.as_view(), name='update-me'),

    path('<str:username>/register_pet/', RegisterPetView.as_view(), name='register-pet'),
    path('<str:username>/<int:pk>/', PetDetaislView.as_view(), name='pet-details'),
    path('<str:username>/<int:pk>/update/', UpdatePetView.as_view(), name='update-pet'),
    path('<str:username>/<int:pk>/delete/', DeletePetView.as_view(), name='delete-pet'),
]
