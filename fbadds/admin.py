from django.contrib import admin
from .models import Page, Adds

# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pageid')


class AddsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_time', 'likes', 'shares', 'comments')


admin.site.register(Page, PageAdmin)
admin.site.register(Adds, AddsAdmin)
