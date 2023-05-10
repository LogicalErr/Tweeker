from django.urls import path
from . import views
urlpatterns = [
    path("", views.home_view, name="home View"),
    path("tweets/", views.tweet_list_view, name="tweet list View"),
    path("create-tweet/", views.tweet_create_view, name="create tweet"),
    path("tweets/<int:tweet_id>", views.tweet_detail_view, name="tweet detail View"),
    path("api/tweets/<int:tweet_id>/delete", views.tweet_delete_view, name="tweet delete View"),
]