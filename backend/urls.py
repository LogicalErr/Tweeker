from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # path("token/", token_obtain_pair, name="token_obtain_pair"),
    # path("token/refresh/", token_refresh, name="token_refresh"),
    path("", include(("tweets.urls", "tweets"), namespace="tweets")),
    path("profiles/", include(("profiles.urls", "profiles"), namespace="profiles")),
    path("api/v1/profiles/", include("profiles.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
