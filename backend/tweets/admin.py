from django.contrib import admin
from tweets.models import Tweet, TweetLike


class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


class TweetAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "timestamp"]
    search_fields = ["user__username", "content",]
    list_filter = ["timestamp"]

    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetAdmin)
