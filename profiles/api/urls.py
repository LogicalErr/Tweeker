from django.urls import path
from profiles.api import views

'''
CLIENT
Base ENDPOINT /api/v1/profiles/
'''

urlpatterns = [
    path("edit/", views.EditProfileView.as_view()),
    path("<str:username>/", views.ProfileDetailView.as_view()),
    path("<str:username>/follow/", views.ProfileDetailView.as_view()),
]
