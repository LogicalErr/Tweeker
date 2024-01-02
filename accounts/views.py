from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings


def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect(settings.HOME_PAGE_URL)
    context = {
        "form": form,
        "btn_label": "Login",
        "title": "Login To Your Account"
    }
    return render(request, "accounts/auth.html", context)


def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        login(request, user)
        return redirect(settings.HOME_PAGE_URL)
    context = {
        "form": form,
        "btn_label": "Signup",
        "title": "Register An Account"
    }
    return render(request, "accounts/auth.html", context)


def logout_view(request, *args, **kwargs):
    # if your is not authenticated it should redirect to login page
    if not isinstance(request.user, User):
        return redirect(settings.LOGIN_URL)

    if request.method == "POST":
        logout(request)
        return redirect(settings.LOGIN_URL)
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Logout",
        "title": "Logout"
    }
    return render(request, "accounts/auth.html", context)
