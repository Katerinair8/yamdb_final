"""
Модуль определения сериализаторов.
"""

from django.db.models import Avg
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    CurrentUserDefault,
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
    ValidationError,
)

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""

    role = ChoiceField(choices=User.ROLES, default="user")

    class Meta:
        """
        Мета модель определяющая поля выдачи.
        Определяет доступ к полю role.
        """

        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserSignupSerializer(ModelSerializer):
    """Сериализатор регистрации."""

    class Meta:
        """Мета модель определяющая поля выдачи."""

        model = User
        fields = (
            "email",
            "username",
        )

    def validate_username(self, attrs):
        """Метод валидации пользователя."""

        if attrs.lower() == "me":
            raise ValidationError("Попробуй другой username")
        return attrs


class UserTokenReceivingSerializer(ModelSerializer):
    """Сериализатор выдачи токена"""

    confirmation_code = CharField(max_length=200, required=True)
    username = CharField(max_length=200, required=True)

    class Meta:
        """Мета модель определяющая поля выдачи."""

        model = User
        fields = ("username", "confirmation_code")


class ReviewSerializer(ModelSerializer):
    """Сериализатор отзыва"""

    author = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    title = SlugRelatedField(
        read_only=True,
        slug_field="id",
    )

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "author",
            "title",
            "text",
            "pub_date",
            "score",
        )
        model = Review

    def validate(self, attrs):
        request = self.context["request"]
        if request.method == "POST":
            if Review.objects.filter(
                author=request.user,
                title=request.parser_context["kwargs"]["title_id"],
            ).exists():
                raise ValidationError(
                    "Невозможно оставить больше одного отзыва на произведение!"
                )
        return attrs


class CommentSerializer(ModelSerializer):
    """Сериализатор комментария"""

    author = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    review = SlugRelatedField(
        read_only=True,
        slug_field="id",
    )

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "author",
            "review",
            "text",
            "pub_date",
        )
        model = Comment


class GenreSerializer(ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = ("name", "slug")
        model = Genre


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = ("name", "slug")
        model = Category


class TitleSerializer(ModelSerializer):
    """Сериализатор для модели Title"""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField(read_only=True)

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "name",
            "year",
            "category",
            "genre",
            "description",
            "rating",
        )
        model = Title
        ordering = ["-id"]

    def get_rating(self, obj):
        """Расчет средней оценки для произведения"""
        return obj.reviews.all().aggregate(Avg("score"))["score__avg"]


class TitleSerializerCreate(TitleSerializer):
    """Сериализатор создания  Title"""

    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        """Мета модель определяющая поля выдачи."""

        fields = (
            "id",
            "name",
            "year",
            "category",
            "genre",
            "description",
        )
        model = Title

        ordering = ["-id"]
