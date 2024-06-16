from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from api.permissions import IsAdminOrReadOnly


class BaseCategoryGenreViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Базовый класс для взаимодействия с категориями и жанрами."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('slug',)
