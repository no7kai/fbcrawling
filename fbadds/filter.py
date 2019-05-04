from .models import Page
import django_filters


class PageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Page
        fields = [
            'name',
        ]
