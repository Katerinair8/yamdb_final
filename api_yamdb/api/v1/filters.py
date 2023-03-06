"""Кастомный фильтр для представления Title.
"""
from django_filters import CharFilter, FilterSet, NumberFilter
from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтры по всем полям модели Title."""

    name = CharFilter(field_name="name", lookup_expr="contains")
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug", lookup_expr="exact")
    year = NumberFilter(field_name="year")

    class Meta:
        model = Title
        fields = ("category", "genre", "name", "year")
