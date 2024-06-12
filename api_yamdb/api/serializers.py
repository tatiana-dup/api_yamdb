import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.utils import send_conform_mail
from reviews.models import Category, Genre, Title


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError(
                "Вы не можете выбрать юзернейм me, выберите другой юзернейм.")
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise ValidationError(
                f"Юзернейм {value} не соответствует паттерну {pattern}.")
        return value

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        if user_by_email and user_by_email.username != username:
            raise ValidationError("Пользователь с таким емейл уже существует, "
                                  "введите верный username.")
        if user_by_username and user_by_username.email != email:
            raise ValidationError(f"Юзернейм {username} уже занят, выберите "
                                  "другой юзернейм.")
        return data

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']

        user_by_email = User.objects.filter(email=email).first()

        if user_by_email:
            send_conform_mail(user_by_email)
            return user_by_email

        user = User.objects.create(
            email=email,
            username=username
        )
        send_conform_mail(user)
        return user


class UsersForAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
