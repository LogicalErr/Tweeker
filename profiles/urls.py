from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>", views.profile_detail_view, name="tweets profile view")
]
