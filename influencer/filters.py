from .models import Post
import django_filters


class PostFilter(django_filters.FilterSet):
    message = django_filters.CharFilter(lookup_expr='icontains')
    created__lt = django_filters.DateTimeFilter(
        field_name='created',
        lookup_expr='lt')
    created__gt = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gt')
    likes__lte = django_filters.NumberFilter(
        field_name='likes',
        lookup_expr='lt')
    likes__gte = django_filters.NumberFilter(
        field_name='likes',
        lookup_expr='gt')

    class Meta:
        model = Post
        fields = [
            'message',
            'created__lt',
            'created__gt',
            'likes__lte',
            'likes__gte',
        ]
