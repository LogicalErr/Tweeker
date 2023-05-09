from django.contrib import admin
from .models import Tweet
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username", "content", "user_email"]
    class Meta:
        model = Tweet
admin.site.register(Tweet, TweetAdmin)