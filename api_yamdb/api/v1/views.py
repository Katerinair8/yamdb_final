"""
Модуль определения представлений.
"""
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permission import (
    IsAdministrator,
    IsAdminOnly,
    IsAuthorOrIsStaffPermission,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerCreate,
    UserSerializer,
    UserSignupSerializer,
    UserTokenReceivingSerializer,
)
from .token import sending_registration_code
from .viewsets import ListCreateDeleteViewSet


class UserViewSet(ModelViewSet):
    """Класс представления пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    filter_fields = ("username",)
    permission_classes = (
        IsAuthenticated,
        IsAdministrator,
    )

    @action(
        detail=False,
        methods=("GET", "PATCH"),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Метод генерации ссылки users/me/ и заменяет его на {username}.
        Помимо этого позволяет пользователю изменять свои данные."""
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid() and (
            request.user.role == "user" or request.user.role == "moderator"
        ):
            if (
                serializer.validated_data.get("role") == "user"
                or serializer.validated_data.get("role") == "moderator"
            ):
                return Response(
                    _("Не надо пытаться менять свою роль"),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserAPIView(APIView):
    """Класс представления регистрации пользователя."""

    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request):
        """Метод проверки данных и генерации писем для активации."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sending_registration_code(serializer)
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )


class GetTokenAPIView(APIView):
    """Класс представления для выдачи токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод проверки confirmation_code и выдачи токена API."""
        serializer = UserTokenReceivingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get("username")
        )
        if default_token_generator.check_token(
            user, serializer.validated_data.get("confirmation_code")
        ):
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
        return Response(
            {"confirmation_code": "Некорректный код подтверждения!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ReviewViewSet(ModelViewSet):
    """Класс представления ревью."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffPermission,
    )

    def get_queryset(self):
        """Метод обработки запроса."""
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Метод предопределения автора."""
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Класс представления комментария."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffPermission,
    )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Метод обработки запроса."""
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Метод предопределения автора."""
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(ListCreateDeleteViewSet):
    """ViewSet для эндпойнта /genre/
    c пагинацией и поиском по полю name"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOnly,
    )
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(ListCreateDeleteViewSet):
    """ViewSet для эндпойнта /Category/
    c пагинацией и поиском по полю name"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOnly,
    )


class TitleViewSet(ModelViewSet):
    """Отображение действий с произведениями"""

    http_method_names = ["get", "post", "delete", "patch"]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOnly,
    )
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Метод предопределения сериализатора в зависимости от запроса."""
        if self.action in ("list", "retrieve"):
            return TitleSerializer
        return TitleSerializerCreate
