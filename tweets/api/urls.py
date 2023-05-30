from django.urls import path
from . import views

'''
CLIENT
Base ENDPOINT /api/tweets/
'''

urlpatterns = [
    path("", views.tweet_list_view, name="tweet list view"),
    path("action/", views.tweet_action_view, name="tweet action view"),
    path("create/", views.tweet_create_view, name="create tweet"),
    path("<int:tweet_id>/", views.tweet_detail_view, name="tweet detail view"),
    path("<int:tweet_id>/delete/", views.tweet_delete_view, name="tweet delete view"),
    path("feed/", views.tweet_feed_view, name="tweet feed view"),
]