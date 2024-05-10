from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'email', 'birth']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['pk','username', 'profile']  # Включаем профиль в список полей

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)  # Извлекаем данные профиля из validated_data
        user = User.objects.create(**validated_data)  # Создаем пользователя
        if profile_data:
            Profile.objects.create(user=user, **profile_data)  # Создаем профиль для пользователя
        return user