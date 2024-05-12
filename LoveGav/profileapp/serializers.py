from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Profile, Pet, Mood, Heat
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

class PetSerializer(serializers.ModelSerializer):
    #поле owner скрыто и заполняется данными текущего пользователя
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ('owner',)

class MoodSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        default=None
    )

    def validate_pet(self, value):
        pet_id = self.context['view'].kwargs['pk']
        return get_object_or_404(Pet, pk=pet_id)
    class Meta:
        model = Mood
        fields = '__all__'
        read_only_fields = ('pet',)

class HeatSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        default=None
    )

    def validate_pet(self, value):
        pet_id = self.context['view'].kwargs['pk']
        return get_object_or_404(Pet, pk=pet_id)
    class Meta:
        model = Heat
        fields = '__all__'
        read_only_fields = ('pet',)
