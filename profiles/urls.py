from django.urls import path
from profiles import views

urlpatterns = [
    path("edit", views.profile_update_view, name="user_update_profile_view"),
    path("<str:username>", views.profile_detail_view, name="user_profile_view")
]
