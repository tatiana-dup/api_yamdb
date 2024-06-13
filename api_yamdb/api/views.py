from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView


from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    UsersForAdminSerializer
)
from reviews.models import Category, Genre, Title, Review
from api.permissions import AllowedToEditOrReadOnly


User = get_user_model()


class UserSignupView(APIView):
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


class CreateOrListUsersByAdminViewSet(mixins.CreateModelMixin,
                                      mixins.ListModelMixin,
                                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersForAdminSerializer
    # permission_classes = Нужен пермишен для пользователя с ролью админа
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AllowedToEditOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AllowedToEditOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
