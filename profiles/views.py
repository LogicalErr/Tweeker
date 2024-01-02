from django.shortcuts import render, redirect
from django.http import Http404
from profiles.models import Profile
from profiles.forms import ProfileForm
from django.conf import settings
from django.contrib.auth.models import User


def profile_update_view(request, *args, **kwargs):
    if not isinstance(request.user, User):
        return redirect(settings.LOGIN_URL)
    user = request.user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
    user_profile = user.profile
    form = ProfileForm(request.POST or None, instance=user_profile, initial=user_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile_obj.save()
    context = {
        "form": form,
        "btn_label": "Save",
        "title": "Update Profile"
    }
    return render(request, "profiles/form.html", context)


def profile_detail_view(request, username, *args, **kwargs):
    user = request.user
    is_following = False

    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        profile = None
        raise Http404

    if isinstance(user, User):
        is_following = user in profile.followers.all()
    context = {
        "username": username,
        # "profile": profile,
        # "is_following": is_following
    }
    return render(request, "profiles/detail.html", context)
