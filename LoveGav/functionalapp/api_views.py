from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from blogapp.permissions import IsAuthorOrReadOnly
from functionalapp.models import Playground, Question, Answer
from functionalapp.serializers import PlaygroundSerializer, QuestionSerializer, AnswerSerializer, PetSerializer
from profileapp.models import Pet


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

    Полный CRUD для сущностей вопросов пользователей
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

    Полный CRUD для сущностей ответов на вопросы пользователей
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


class СalorieСalculatorApiView(APIView):
    """
    Представление для расчета калорий
    Ожидаемые данные для POST-запроса:
    - weight - вес питомца;
    - calorie_content - калорийность корма (ккал/кг);
    - коэффициенты активности (true/false):
        k1 - Light physical activity;
        k2 - Hard work;
        k3 - Without physical activity;
        k4 - Feeds the puppies;
        k5 - Just born (0-3 months);
        k6 - Large breed puppy (3-9 months old);
        k7 - Large breed puppy (9-24 months old);
        k8 - Puppy of medium and small breeds (3-6 months);
        k9 - Puppy of medium and small breeds (3-6 months);
        k10 - Puppy of medium and small breeds (6-12 months).
    Пример:
    {
    "weight": 5.5,
    "calorie_content": 4000,
    "k1": true
    }
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def calculate_calories_for_pet(weight, calorie_content, kkk):
        results = {}
        kkk_dict = {'k1': 1.2,
                    'k2': 3,
                    'k3': 0.8,
                    'k4': 2.4,
                    'k5': 2,
                    'k6': 1.6,
                    'k7': 1.2,
                    'k8': 1.6,
                    'k9': 1.6,
                    'k10': 1.2}

        if weight < 2:
            result = 2 * (70 * weight ** 0.75)
        else:
            result = 2 * (30 * weight + 70)

        count = 1
        for k in kkk:
            if k == True:
                result *= kkk_dict['k' + str(count)]
            count += 1

        results['calories_per_day'] = result

        one_calorie = 1000 / calorie_content
        results['grams'] = result * one_calorie

        return results

    def get(self, request):
        try:
            pets = Pet.objects.filter(owner=request.user)
            context = {
                "pets": PetSerializer(pets, many=True).data,
            }
        except Pet.DoesNotExist:
            context = {
                "pets": "You haven't listed any pets yet",
            }

        return Response(context)

    def post(self, request):
        data = request.data
        weight = data.get('weight')
        calorie_content = data.get('calorie_content')
        kkk = [data.get('k' + str(i)) for i in range(1, 11)]

        if weight is None or calorie_content is None:
            return Response({"error": "Weight and calorie content are required"}, status=status.HTTP_400_BAD_REQUEST)

        results = self.calculate_calories_for_pet(weight, calorie_content, kkk)

        return Response(results, status=status.HTTP_200_OK)
