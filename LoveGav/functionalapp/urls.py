from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HelloView
from .views import СalorieСalculatorView, DogPlaygroundsView, QuestionListView, CreateQuestionView, QuestionDetailsView, \
    QuestionUpdateView, QuestionDeleteView, AnswerDeleteView
from .api_views import PlaygroundListView, QuestionViewSet, AnswerViewSet, СalorieСalculatorApiView

app_name = "functionalapp"

routers = DefaultRouter()
routers.register("questions", QuestionViewSet, basename='question')
routers.register("answers", AnswerViewSet, basename='answer')

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('calculator/', СalorieСalculatorView.as_view(), name='calculator'),
    path('playgrounds/', DogPlaygroundsView.as_view(), name="playground-list"),
    path('questions/list/', QuestionListView.as_view(), name="questions-list"),
    path('questions/create/', CreateQuestionView.as_view(), name="question-create"),
    path('questions/<int:pk>/', QuestionDetailsView.as_view(), name="question-details"),
    path('questions/<int:pk>/update/', QuestionUpdateView.as_view(), name="question-update"),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name="question-delete"),
    path('answers/<int:pk>/delete/', AnswerDeleteView.as_view(), name="answer-delete"),

    path('api/', include(routers.urls)),
    path('api/playgrounds/', PlaygroundListView.as_view()),
    path('api/questions/<int:pk>/answers/', AnswerViewSet.as_view({'get': 'list',
                                                                   'post': 'create'})),
    path('api/questions/<int:pk>/answers/<int:answer_pk>/', AnswerViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='answer-detail'),
    path('api/calculate-calories/', СalorieСalculatorApiView.as_view(), name='calculate_calories'),
]
