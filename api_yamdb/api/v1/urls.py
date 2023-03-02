"""
Модуль определения публикуемых страниц.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    CreateUserAPIView,
    GenreViewSet,
    GetTokenAPIView,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

app_name = "api"

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")


token = [
    path("signup/", CreateUserAPIView.as_view(), name="signup"),
    path("token/", GetTokenAPIView.as_view(), name="token"),
]


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include(token)),
]
