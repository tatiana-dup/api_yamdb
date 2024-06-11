from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet,
                       CreateOrListUsersByAdminViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       UserSignupView)


router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', CreateOrListUsersByAdminViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', UserSignupView.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),
]
