from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import User
from .permissions import IsOwnerOrStaffReadOnly
from .serializers import UserSerializer


@api_view(['GET', 'POST'])
def users_list(request):
    """
    Просмотр списка всех пользователей или создание нового пользователя
    """

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Вызываем метод create() в UserSerializer для создания пользователя и профиля
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    Create, update, delete и detail для конкретного пользователя
    """
    permission_classes = (IsOwnerOrStaffReadOnly,)
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Вызываем метод update() в UserSerializer для редактирования профиля
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
