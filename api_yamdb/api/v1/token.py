"""Модуль генерации и отправки кода подтверждения."""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from users.models import User


def confirmation_code(self):
    """Формирует код подтвержденияe-mail."""
    user = get_object_or_404(User, username=self)
    return default_token_generator.make_token(user)


def sending_registration_code(self):
    """Формирует и отправляет письмо с кодом подтверждения."""
    send_mail(
        "Подтверждение почты",
        (
            f"Ваш код подтверждения для авторизации:"
            f"{confirmation_code(self.validated_data.get('username'))}"
        ),
        "from@example.com",
        [self.validated_data.get("email")],
        fail_silently=False,
    )
