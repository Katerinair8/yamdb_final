"""Модуль абстрактных моделей."""
from django.core.validators import validate_slug
from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель для Category и Genre. Добавляет имя и слаг."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True, validators=[validate_slug], max_length=50
    )
    constraints = [
        models.UniqueConstraint(
            fields=["name", "slug"], name="unique_name_slug"
        )
    ]

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["name"]
        abstract = True
