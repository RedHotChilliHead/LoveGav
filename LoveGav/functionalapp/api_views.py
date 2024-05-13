from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from blogapp.permissions import IsAuthorOrReadOnly
from functionalapp.models import Playground, Question, Answer
from functionalapp.serializers import PlaygroundSerializer, QuestionSerializer, AnswerSerializer


class PlaygroundListView(ListAPIView):
    """
    Представление просмотра списка площадок для собак
    """
    queryset = Playground.objects.all()
    serializer_class = PlaygroundSerializer

    filter_backends = [SearchFilter]
    search_fields = [
        "town",
        "address",
        "description"
    ]

class QuestionViewSet(ModelViewSet):
    """
    Набор представлений для действий над Question.

    Полный CRUD для сущностей вопросов
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = [
        "data",
    ]
    # поиск по нескольким полям сразу
    search_fields = ['head', 'body']
    # поиск по конкретному полю
    filterset_fields = [
        "author",
        "data",
    ]

    def perform_create(self, serializer):
        # При создании новой записи, устанавливаем автора текущего запроса
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        # Переопределяем метод создания, чтобы передать автора в serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AnswerViewSet(ModelViewSet):
    """
    Набор представлений для действий над Answer.

    Полный CRUD для сущностей постов
    """

    def get_queryset(self):
        question = Question.objects.get(pk=self.kwargs['pk'])
        return Answer.objects.filter(question=question)

    serializer_class = AnswerSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    lookup_url_kwarg = 'answer_pk'

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = [
        "data",
    ]

    # поиск по конкретному полю
    filterset_fields = [
        "author",
        "body",
        "data",
    ]

    def perform_create(self, serializer):
        # При создании новой записи, устанавливаем автора текущего запроса
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        # Переопределяем метод создания, чтобы передать автора в serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)