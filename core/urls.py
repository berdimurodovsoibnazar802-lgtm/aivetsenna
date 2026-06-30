from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("twin/", views.digital_twin, name="digital_twin"),
    path("tahlil/", views.ai_analysis, name="ai_analysis"),
    path("tavsiyalar/", views.recommendations, name="recommendations"),
    path("profil/", views.profile_settings, name="profile_settings"),
]
