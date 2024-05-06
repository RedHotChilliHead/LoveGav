from django.urls import path
from django.contrib.auth.views import LoginView

from .views import RegisterView, logout_view, UpdateMeView, UserDetaislView, DeleteUserView
from .views import RegisterPetView, PetDetaislView, UpdatePetView, DeletePetView
from .views import CreateMoodView, DeleteMoodView, CreateHeatView, DeleteHeatView, CreateTreatmentView, DeleteTreatmentView

app_name = "profileapp"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',
         LoginView.as_view(template_name='profileapp/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', logout_view, name='logout'),

    path('<str:username>/', UserDetaislView.as_view(), name='user-details'),
    path('<str:username>/update/', UpdateMeView.as_view(), name='update-me'),
    path('<str:username>/<int:pk>/delete/', DeleteUserView.as_view(), name='delete-me'),

    path('<str:username>/register_pet/', RegisterPetView.as_view(), name='register-pet'),
    path('<str:username>/<int:pk>_pet/', PetDetaislView.as_view(), name='pet-details'),
    path('<str:username>/<int:pk>_pet/update/', UpdatePetView.as_view(), name='update-pet'),
    path('<str:username>/<int:pk>_pet/delete/', DeletePetView.as_view(), name='delete-pet'),

    path('<str:username>/<int:pk>_pet/mood-create/', CreateMoodView.as_view(), name='create-mood'),
    path('<str:username>/<int:pk>_mood/delete/', DeleteMoodView.as_view(), name='delete-mood'),

    path('<str:username>/<int:pk>_pet/heat-create/', CreateHeatView.as_view(), name='create-heat'),
    path('<str:username>/<int:pk>_heat/delete/', DeleteHeatView.as_view(), name='delete-heat'),

    path('<str:username>/<int:pk>_pet/treatment-create/', CreateTreatmentView.as_view(), name='create-treatment'),
    path('<str:username>/<int:pk>_treatment/delete/', DeleteTreatmentView.as_view(), name='delete-treatment'),
]
