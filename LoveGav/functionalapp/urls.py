from django.urls import path
from .views import HelloView
from .views import СalorieСalculatorView, DogPlaygroundsView, QuestionListView, CreateQuestionView, QuestionDetailsView, \
    QuestionUpdateView, QuestionDeleteView

app_name = "functionalapp"

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('calculator/', СalorieСalculatorView.as_view(), name='calculator'),
    path('playgrounds/', DogPlaygroundsView.as_view(), name="playground-list"),
    path('questions/', QuestionListView.as_view(), name="question-list"),
    path('questions/create/', CreateQuestionView.as_view(), name="question-create"),
    path('questions/<int:pk>/', QuestionDetailsView.as_view(), name="question-details"),
    path('questions/<int:pk>/update', QuestionUpdateView.as_view(), name="question-update"),
    path('questions/<int:pk>/delete', QuestionDeleteView.as_view(), name="question-delete"),
]
