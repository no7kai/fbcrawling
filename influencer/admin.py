from django.contrib import admin
from .models import Influencer, Post


class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uid', 'followers')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'influencer', 'message', 'postid')  # Field gi can hien thi thi them vao day


admin.site.register(Influencer, InfluencerAdmin)
admin.site.register(Post, PostAdmin)
