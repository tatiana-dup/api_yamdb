from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    SignupSerializer,
    TitleSerializer,
    UsersForAdminSerializer
)
from reviews.models import Category, Genre, Title


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
