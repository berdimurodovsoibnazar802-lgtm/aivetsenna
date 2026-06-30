from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "full_name", "gender", "age", "height_cm", "weight_kg",
            "glucose_mg_dl", "systolic_bp", "diastolic_bp",
            "daily_steps", "sleep_hours", "takes_medication",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Ism Familiya"}),
            "gender": forms.Select(),
            "age": forms.NumberInput(attrs={"placeholder": "47"}),
            "height_cm": forms.NumberInput(attrs={"placeholder": "164"}),
            "weight_kg": forms.NumberInput(attrs={"placeholder": "82"}),
            "glucose_mg_dl": forms.NumberInput(attrs={"placeholder": "186", "step": "0.1"}),
            "systolic_bp": forms.NumberInput(attrs={"placeholder": "130"}),
            "diastolic_bp": forms.NumberInput(attrs={"placeholder": "85"}),
            "daily_steps": forms.NumberInput(attrs={"placeholder": "3200"}),
            "sleep_hours": forms.NumberInput(attrs={"placeholder": "5.8", "step": "0.1"}),
        }
