from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView

from .views import RegisterView, logout_view, UpdateMeView, UserDetaislView, DeleteUserView
from .views import RegisterPetView, PetDetaislView, UpdatePetView, DeletePetView
from .views import CreateMoodView, DeleteMoodView, CreateHeatView, DeleteHeatView, CreateTreatmentView, \
    DeleteTreatmentView, DairyDetaislView, DairyPetDataExportView

from .api_views import users_list, UserDetailView, PetViewSet, MoodViewSet, HeatViewSet, TreatmentViewSet

app_name = "profileapp"

routers = DefaultRouter()
routers.register("pets", PetViewSet, basename='pet')
routers.register("moods", MoodViewSet, basename='mood')
routers.register("heats", HeatViewSet, basename='heat')
routers.register("treatments", TreatmentViewSet, basename='treatment')

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
    path('<str:username>/<int:pk>_pet/dairy/', DairyDetaislView.as_view(), name='dairy-pet-details'),
    path('<str:username>/<int:pk>_pet/update/', UpdatePetView.as_view(), name='update-pet'),
    path('<str:username>/<int:pk>_pet/delete/', DeletePetView.as_view(), name='delete-pet'),

    path('<str:username>/<int:pk>_pet/mood-create/', CreateMoodView.as_view(), name='create-mood'),
    path('<str:username>/<int:pk>_mood/delete/', DeleteMoodView.as_view(), name='delete-mood'),

    path('<str:username>/<int:pk>_pet/heat-create/', CreateHeatView.as_view(), name='create-heat'),
    path('<str:username>/<int:pk>_heat/delete/', DeleteHeatView.as_view(), name='delete-heat'),

    path('<str:username>/<int:pk>_pet/treatment-create/', CreateTreatmentView.as_view(), name='create-treatment'),
    path('<str:username>/<int:pk>_treatment/delete/', DeleteTreatmentView.as_view(), name='delete-treatment'),

    path('<str:username>/<int:pk>_pet/export/', DairyPetDataExportView.as_view(), name='export-dairy'),

    path('api/', include(routers.urls)),
    path('api/pets/<int:pk>/moods/', MoodViewSet.as_view({'get': 'list',
                                                          'post': 'create'})),
    path('api/pets/<int:pk>/moods/<int:mood_pk>/', MoodViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='mood-detail'),
    path('api/pets/<int:pk>/heats/', HeatViewSet.as_view({'get': 'list',
                                                          'post': 'create'})),
    path('api/pets/<int:pk>/heats/<int:heat_pk>/', HeatViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='heat-detail'),
    path('api/pets/<int:pk>/treatments/', TreatmentViewSet.as_view({'get': 'list',
                                                          'post': 'create'})),
    path('api/pets/<int:pk>/treatments/<int:treatment_pk>/', TreatmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='treatment-detail'),

    path('api/users/', users_list),
    path('api/users/<int:pk>/', UserDetailView.as_view()),

]
