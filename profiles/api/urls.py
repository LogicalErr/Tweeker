from django.urls import path
from profiles.api import views

'''
CLIENT
Base ENDPOINT /api/v1/profiles/
'''

urlpatterns = [
    path("<str:username>", views.profile_detail_api_view),
    path("<str:username>/follow", views.profile_detail_api_view),
]
