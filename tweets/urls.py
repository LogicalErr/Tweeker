from django.urls import path
from . import views
urlpatterns = [
    path("", views.home_view, name="home View"),
    path("tweets/", views.tweetlist_view, name="tweet list View"),
    path("tweets/<int:tweet_id>", views.tweetdetail_view, name="tweet detail View"),
]