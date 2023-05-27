from django.urls import path
from . import views
urlpatterns = [
    path("edit", views.profile_update_view, name="user update profile view"),
    path("<str:username>", views.profile_detail_view, name="user profile view")
]
