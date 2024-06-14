import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from api.mixins import UsernameValidatorMixin
from reviews.const import MAX_SCORE_VALUE, MIN_SCORE_VALUE
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


User = get_user_model()


class SignupSerializer(UsernameValidatorMixin, serializers.Serializer):
    """
    Сериализатор для обработки запроса на получение кода подтверждения.
    """
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message=("В юзернейме допустимо использовать только "
                     "латинские буквы, цифры или @/./+/-/_ ."))])


class UsersSerializer(UsernameValidatorMixin, serializers.ModelSerializer):
    """Базовый сериализатор для модели пользователя."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=("В юзернейме допустимо использовать только "
                         "латинские буквы, цифры или @/./+/-/_ .")),
            UniqueValidator(queryset=User.objects.all(),
                            message='Этот юзернейм уже занят.')
        ])
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Этот емейл уже занят.')
        ])
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UsersForAdminSerializer(UsersSerializer):
    """
    Сериализатор для модели пользователя, предназначенный для запросов,
    полученных от администратора.
    """


class UsersForMeSerializer(UsersSerializer):
    """
    Сериализатор для модели пользователя, предназначенный для запросов,
    полученных от обычного пользователя.
    """
    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)


class ObtainTokenSerializer(serializers.Serializer):
    """Сериализатор для генерации токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

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
        return {
            'token': str(refresh.access_token),
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для Жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для Произведений как для чтения, так и для записи."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data
        response['category'] = CategorySerializer(instance.category).data
        return response


class ReviewSerializer(serializers.ModelSerializer):
    """Формирование информации об отзыве."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.context.get('view').kwargs.get('title_id')
        )

    def get_user(self):
        return self.context['request'].user

    def get_method(self):
        return self.context['request'].method

    def validate_score(self, value):
        if (value > MAX_SCORE_VALUE or value < MIN_SCORE_VALUE):
            raise serializers.ValidationError(
                f'Оценка не попадает в допустимый диапазон: {MIN_SCORE_VALUE}'
                f': {MAX_SCORE_VALUE}'
            )
        return value

    def validate(self, data):
        if (
                Review.objects.filter(
                    title=self.get_title(),
                    author=self.get_user()
                ).exists()
                and self.get_method() == 'POST'
        ):
            raise serializers.ValidationError(
                'Для этого произведения ты уже сделал отзыв!'
            )
        return data

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        model = Review
        read_only_fields = ('pub_date',)
        extra_kwargs = {'score': {'required': True}}


class CommentSerializer(serializers.ModelSerializer):
    """Формирование информации о комменте."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('pub_date',)
