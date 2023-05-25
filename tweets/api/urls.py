from django.urls import path
from . import views

'''
CLIENT
Base ENDPOINT /api/tweets/
'''

urlpatterns = [
    path("", views.tweet_list_view, name="tweet list View"),
    path("action/", views.tweet_action_view, name="tweet action View"),
    path("create/", views.tweet_create_view, name="create tweet"),
    path("<int:tweet_id>/", views.tweet_detail_view, name="tweet detail View"),
    path("<int:tweet_id>/delete/", views.tweet_delete_view, name="tweet delete View"),
]