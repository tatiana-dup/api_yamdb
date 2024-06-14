from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from api.permissions import AdminOnly, AdminOrReadOnly
# from api.permissions_test import RolePermission
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    ObtainTokenSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    TitleSerializerWrite,
    UsersForAdminSerializer,
    UsersForMeSerializer
)
from reviews.models import Category, Genre, Title, Review
from api.permissions import AllowedToEditOrReadOnly


User = get_user_model()


class UserSignupView(APIView):
    """Класс для обработки запроса на получение кода подтверждения."""
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "email": user.email,
                "username": user.username
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Класс для обработки запросов, связанных с пользователем."""
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UsersForAdminSerializer
    permission_classes = (AdminOnly,)
    # permission_classes = (RolePermission,)
    # required_roles = ['admin',]
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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

class ObtainTokenView(APIView):
    """Класс для обработки запроса на получение токена."""
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.get_token_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerWrite
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Отображение отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = (AllowedToEditOrReadOnly,)
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
    permission_classes = (AllowedToEditOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
