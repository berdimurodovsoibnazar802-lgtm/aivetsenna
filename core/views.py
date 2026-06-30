from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import ProfileForm
from accounts.models import Profile


def landing(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")
    return render(request, "core/landing.html")


@login_required
def onboarding(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.onboarding_complete = True
            profile.digital_twin_created = True
            profile.save()
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "core/onboarding.html", {"form": form})


@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if not profile.onboarding_complete:
        return redirect("core:onboarding")
    context = {
        "profile": profile,
        "today_tip": "Bugun 30 daqiqa piyoda yurish va uyqu rejimini yaxshilashni tavsiya etiladi.",
    }
    return render(request, "core/dashboard.html", context)


@login_required
def digital_twin(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    scenarios = [
        "Har kuni 30 daqiqa",
        "Shirin ichimliklarni kamaytirsam",
        "Uyquni 8 soat qilsam",
        "Dorini vaqtida ichsam",
        "Vaznimni 5 kg kamaytirsam",
    ]
    context = {"profile": profile, "scenarios": scenarios}
    return render(request, "core/digital_twin.html", context)


@login_required
def ai_analysis(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    context = {
        "profile": profile,
        "target_risk": 50,
        "ai_recommendation": "Bugun 30 daqiqa piyoda yurish va uyqu rejimini yaxshilashni tavsiya etiladi.",
    }
    return render(request, "core/ai_analysis.html", context)


@login_required
def recommendations(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    plan_today = [
        "30 daqiqa yurish",
        "Shirin ichimliklarni cheklash",
        "Glyukozani qayta o'lchash",
    ]
    plan_week = [
        "Har kuni kamida 6 000 qadam",
        "Uyquni 7 soatdan kam qilmaslik",
        "Dorilarni eslatma asosida qabul qilish",
    ]
    context = {
        "profile": profile,
        "plan_today": plan_today,
        "plan_week": plan_week,
    }
    return render(request, "core/recommendations.html", context)


@login_required
def profile_settings(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("core:profile_settings")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "core/profile_settings.html", {"form": form, "profile": profile})
