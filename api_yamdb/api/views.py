from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from api.filters import TitleFilter
from api.permissions import (IsAdmin,
                             IsAdminOrReadOnly,
                             IsAllowedToEditOrReadOnly)
from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             ObtainTokenSerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             SignupSerializer,
                             TitleSerializer,
                             UsersForMeSerializer,
                             UsersSerializer)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class UserSignupView(APIView):
    """
    Класс для обработки запроса на получение кода подтверждения.
    - если пользователя с полученными данными не существует, то он будет
    создан, и на его email отправлено письмо с кодом подтверждения;
    - если пользователь уже существует, то на его email будет отправлено письмо
    с кодом подтверждения.
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            "email": user.email,
            "username": user.username
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Класс для обработки запросов, связанных с пользователем."""
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UsersForMeSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UsersForMeSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ObtainTokenView(APIView):
    """Класс для обработки запроса на получение токена."""
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.get_token_for_user(user)
        return Response(token, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Класс для взаимодействия с Категориями."""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('id',)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Класс для взаимодействия с Жанрами."""
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('id',)


class TitleViewSet(viewsets.ModelViewSet):
    """Класс для взаимодействия с Произведениями."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = TitleFilter
    ordering = ('id',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Отображение отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAllowedToEditOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Отображение коммента."""

    serializer_class = CommentSerializer
    permission_classes = (IsAllowedToEditOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
