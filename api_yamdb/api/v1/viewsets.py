"""Модуль кастомных вьюсетов."""


from rest_framework.viewsets import GenericViewSet, mixins


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """Представитель для предоставления прав на List, Create, Delete."""

    ...
