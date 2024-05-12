from rest_framework.generics import ListAPIView

from functionalapp.models import Playground
from functionalapp.serializers import PlaygroundSerializer


class PlaygroundListView(ListAPIView):
    """
    Представление просмотра списка площадок для собак
    """
    queryset = Playground.objects.all()
    # pagination_class = 15
    serializer_class = PlaygroundSerializer