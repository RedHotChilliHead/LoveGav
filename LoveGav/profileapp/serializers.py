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

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.profile.email = profile_data.get('email', instance.profile.email)
        instance.profile.bio = profile_data.get('bio', instance.profile.bio)
        instance.profile.birth = profile_data.get('birth', instance.profile.birth)
        instance.profile.save()
        instance.save()
        return instance