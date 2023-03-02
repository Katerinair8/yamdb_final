"""Модуль моделей."""
from datetime import datetime

from core.models import CreatedModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Category(CreatedModel):
    """Модель для Category. Наследуется из Core."""

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.slug


class Genre(CreatedModel):
    """Модель для Genre. Наследуется из Core."""

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(_("Название произведения"), max_length=250)
    year = models.IntegerField(
        _("Год создания"),
        help_text=_("Год в формате 2022"),
        db_index=True,
        validators=[
            MaxValueValidator(
                datetime.now().year, message=_("Такой год еще не наступил!")
            ),
            MinValueValidator(1000, message=_("Слишком ранняя дата!")),
        ],
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    description = models.TextField(_("Описание"), blank=True)

    class Meta:
        verbose_name = _("Произведение")
        verbose_name_plural = _("Произведения")
        ordering = ["name", "year"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_name_category"
            )
        ]

    def __str__(self):
        return {self.name}


class GenreTitle(models.Model):
    """Таблица для ManyToMany связи жанра и произведения"""

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.title}"


class Review(models.Model):
    """Модель ревью."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        _("Дата создания отзыва"), auto_now_add=True, db_index=True
    )
    score = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        validators=[
            MaxValueValidator(10, message=_("Максимальная оценка - 10")),
            MinValueValidator(1, message=_("Минимальная оценка - 1")),
        ],
    )

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ("-pub_date", "score")
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review_title"
            )
        ]

    def __str__(self):
        return f"{self.text}"[:15]


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        _("Дата комментария к отзыву"), auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = _("Коментарий")
        verbose_name_plural = _("Коментарии")

    def __str__(self):
        return f"{self.text}"[:15]
