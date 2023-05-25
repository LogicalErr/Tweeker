from django.urls import path, include
from . import views

'''
CLIENT
Base ENDPOINT /
'''

urlpatterns = [
    path("", views.tweets_list_view, name="tweets list views"),
    path("<int:tweet_id>", views.tweets_detail_view, name="tweets detail view"),
    path('api/tweets/', include("tweets.api.urls"))
]










