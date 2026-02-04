from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile  # assuming you have a UserProfile model

# =========================
# REGISTER VIEW
# =========================
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile automatically
            UserProfile.objects.get_or_create(user=user)
            login(request, user)  # auto-login after registration
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("blog:post_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# =========================
# LOGIN VIEW
# =========================
def login_view(request):
    next_url = request.GET.get("next", "blog:post_list")
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


# =========================
# LOGOUT VIEW
# =========================
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


# =========================
# PROFILE VIEW
# =========================
@login_required
def profile_view(request):
    # Ensure the user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})
