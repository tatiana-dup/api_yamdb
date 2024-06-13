import jwt
import re
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_conform_mail
from reviews.const import MAX_SCORE_VALUE, MIN_SCORE_VALUE
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


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
                "В юзернейме допустимо использовать только "
                "латинские буквы, цифры или @/./+/-/_ .")
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


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    def validate_username(self, value):
        self.user = get_object_or_404(User, username=value)
        return value

    def validate_confirmation_code(self, value):
        try:
            payload = jwt.decode(
                value, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Код подтверждения истек.")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError(
                "Недействительный код подтверждения.")

        self.username = payload.get('username')
        return value

    def validate(self, data):
        if data.get('username') != self.username:
            raise serializers.ValidationError(
                "Неверный код подтверждения или юзернейм.")
        data['user'] = self.user
        return data

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['write'] = user.role

        return {
            'token': str(refresh.access_token),
        }


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate_score(self, value):
        if MIN_SCORE_VALUE < value < MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                f'Оценка не попадает в допустимый диапазон: {MIN_SCORE_VALUE}'
                f': {MAX_SCORE_VALUE}'
            )
        return value

    class Meta:
        fields = (
            'id',
            'text',
            'score',
            'pub_date',
        )
        model = Review
        read_only_fields = ('pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Ты оставлял отзыв к этому произведению.'
            ),
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('pub_date')
