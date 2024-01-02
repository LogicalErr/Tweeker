from django.urls import path
from tweets.api import views

'''
CLIENT
Base ENDPOINT /api/v1/tweets/
'''

urlpatterns = [
    path("", views.TweetsListView.as_view(), name="tweets_list_view"),
    path("action/", views.TweetActionView.as_view(), name="tweet_action_view"),
    path("create/", views.TweetCreateView.as_view(), name="create tweet"),
    path("<int:tweet_id>/", views.TweetDetailView.as_view(), name="tweet_detail_view"),
    path("<int:tweet_id>/delete/", views.TweetDeleteView.as_view(), name="tweet_delete_view"),
    path("feed/", views.TweetFeedView.as_view(), name="tweet_feed_view"),
]
