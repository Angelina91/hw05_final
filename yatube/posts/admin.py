from django.conf import settings
from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "pub_date",
        "author",
        "group",
    )
    list_editable = ("group",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = settings.EMPTY_VALUE


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    search_fields = "title"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "post",
        "author",
        "text",
        "created",
    )
    search_fields = ("text",)
    list_filter = ("created",)
    empty_value_display = settings.EMPTY_VALUE


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "slug",
    )
    list_editable = ("title",)
    search_fields = ("slug",)
    list_filter = ("title",)
    empty_value_display = settings.EMPTY_VALUE


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)
