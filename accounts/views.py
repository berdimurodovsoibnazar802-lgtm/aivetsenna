from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import Profile


class AppLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


def register(request):
    if request.user.is_authenticated:
        return redirect("core:onboarding")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("core:onboarding")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
