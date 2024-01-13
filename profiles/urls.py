from django.urls import path, include


urlpatterns = [
    path("api/v1/profiles/", include("profiles.api.urls")),
]
