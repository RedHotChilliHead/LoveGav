from rest_framework import serializers
from .models import Playground

class PlaygroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playground
        fields = ['town', 'address', 'description', 'photo']