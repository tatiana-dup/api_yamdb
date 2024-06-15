from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_conform_mail
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from users.validators import validate_username


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """
    Сериализатор для обработки запроса на получение кода подтверждения.
    """
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username])

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        errors = {}
        if user_by_email != user_by_username:
            if user_by_email:
                errors['email'] = [
                    'Этот емейл используется с другим юзернейм.']
            if user_by_username:
                errors['username'] = [
                    f'Юзернейм {username} занят другим пользователем.']
            raise ValidationError(errors)

        data['user'] = user_by_email
        return data

    def create(self, validated_data):
        user = (validated_data.get('user')
                or User.objects.create(
                    email=validated_data.get('email'),
                    username=validated_data.get('username')))
        send_conform_mail(user)
        return user


class UsersSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


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

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        is_confirmation_code_correct = default_token_generator.check_token(
            user, data['confirmation_code'])
        if not is_confirmation_code_correct:
            raise serializers.ValidationError(
                'Недействительный или истекший код подтверждения.')
        data['user'] = user
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

    def validate(self, data):
        if (
                self.get_method() == 'POST'
                and Review.objects.filter(
                    title=self.get_title(),
                    author=self.get_user()
                ).exists()
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
