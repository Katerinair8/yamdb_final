"""Модуль модели пользователя."""
from dataclasses import dataclass

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


@dataclass(frozen=True)
class UserRoles:
    """Класс словаря ролей пользователей."""

    USER: str = "user"
    MODERATOR: str = "moderator"
    ADMIN: str = "admin"


class User(AbstractUser):
    """Расширенная модель пользователя."""

    ROLES = (
        (UserRoles.USER, "user"),
        (UserRoles.MODERATOR, "moderator"),
        (UserRoles.ADMIN, "admin"),
    )
    email = models.EmailField(
        _("Электронная почта"),
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(_("Биография"), max_length=256, blank=True)
    role = models.CharField(
        _("Роль пользователя"), max_length=16, choices=ROLES, default="user"
    )

    REQUIRED_FIELDS = ("email",)

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("id",)

    @property
    def get_role(self):
        """Метод возвращает роль пользователя."""
        return self.role

    @property
    def is_user(self):
        """Метод подтверждает роль пользователя USER."""
        return self.role == UserRoles.USER

    @property
    def is_admin(self):
        """Метод подтверждает роль пользователя ADMIN."""
        return self.role == UserRoles.ADMIN

    @property
    def is_moderator(self):
        """Метод подтверждает роль пользователя MODERATOR."""
        return self.role == UserRoles.MODERATOR

    def __str__(self):
        return self.username
