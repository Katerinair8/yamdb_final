"""
Модуль определения дополнительных прав доступа.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdministrator(BasePermission):
    """
    Разрешения для пользователя с ролью администратор или суперпользователь.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff
        )


class IsAuthorOrIsStaffPermission(BasePermission):
    """Разрешение на редактирование автору и персоналу."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser
            or request.user.is_moderator
        )


class IsAdminOnly(BasePermission):
    """Разрешение для только для администратора."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )
