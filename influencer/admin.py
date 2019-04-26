from django.contrib import admin
from .models import Influencer, Post
from django.db.models import Q


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class UidFilter(InputFilter):
    parameter_name = 'uid'
    title = 'User Uid'

    def queryset(self, request, queryset):
        if self.value() is not None:
            uid = self.value()

            return queryset.filter(
                Q(uid=uid)
            )


class NameFilter(InputFilter):
    parameter_name = 'user'
    title = 'User Name'

    def queryset(self, request, queryset):
        term = self.value()

        if term is None:
            return

        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(name__icontains=bit)
            )

        return queryset.filter(any_name)


class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uid', 'followers')
    list_filter = (UidFilter, NameFilter)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'influencer', 'message', 'postid')


admin.site.register(Influencer, InfluencerAdmin)
admin.site.register(Post, PostAdmin)
