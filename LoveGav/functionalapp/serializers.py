from django.shortcuts import get_object_or_404
from rest_framework import serializers

from profileapp.models import Pet
from .models import Playground, Question, Answer


class PlaygroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playground
        fields = ['town', 'address', 'description', 'photo']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('author',)

class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        default=None
    )

    def validate_question(self, value):
        question_id = self.context['view'].kwargs['pk']
        return get_object_or_404(Question, pk=question_id)
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('question', 'author')

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('name', 'weight')