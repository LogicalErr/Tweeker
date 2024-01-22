from django.urls import path, include

'''
CLIENT
Base ENDPOINT /
'''

urlpatterns = [
    path('api/v1/tweets/', include("tweets.api.urls")),
]
