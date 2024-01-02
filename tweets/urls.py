from django.urls import path, include
from tweets import views

'''
CLIENT
Base ENDPOINT /
'''

urlpatterns = [
    path("", views.home_view, name="home_view"),
    # path("global/", views.tweets_list_view, name="tweets_list_view"),
    path("<int:tweet_id>", views.tweets_detail_view, name="tweets detail view"),
    path('api/v1/tweets/', include("tweets.api.urls")),
]
