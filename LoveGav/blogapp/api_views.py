from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from blogapp.models import Post, Comment
from blogapp.permissions import IsAuthorOrReadOnly
from blogapp.serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    """
    Набор представлений для действий над Post.

    Полный CRUD для сущностей постов
    """

    queryset = Post.objects.all()

    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = [
        "data",
    ]

    # поиск по конкретному полю
    filterset_fields = [
        "author",
        "description",
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


class CommentViewSet(ModelViewSet):
    """
    Набор представлений для действий над Comment.

    Полный CRUD для сущностей постов
    """

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post)

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    lookup_url_kwarg = 'comment_pk'

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

