from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(("tweets.urls", "tweets"), namespace="tweets")),
    # path("profiles/", include(("profiles.urls", "profiles"), namespace="profiles")),
    path("api/v1/profiles/", include("profiles.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
