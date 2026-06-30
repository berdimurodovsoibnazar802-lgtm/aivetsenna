from django.conf import settings
from django.db import models


class Profile(models.Model):
    GENDER_CHOICES = [
        ("male", "Erkak"),
        ("female", "Ayol"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField("F.I.Sh.", max_length=150, blank=True)
    gender = models.CharField("Jinsi", max_length=10, choices=GENDER_CHOICES, default="female")
    age = models.PositiveIntegerField("Yoshi", null=True, blank=True)
    height_cm = models.PositiveIntegerField("Bo'yi (sm)", null=True, blank=True)
    weight_kg = models.PositiveIntegerField("Vazni (kg)", null=True, blank=True)
    glucose_mg_dl = models.FloatField("Qon glyukozasi (mg/dL)", null=True, blank=True)
    systolic_bp = models.PositiveIntegerField("Qon bosimi (yuqori)", null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField("Qon bosimi (pastki)", null=True, blank=True)
    daily_steps = models.PositiveIntegerField("Kunlik qadamlar", null=True, blank=True)
    sleep_hours = models.FloatField("Uyqu davomiyligi (soat)", null=True, blank=True)
    takes_medication = models.BooleanField("Dori qabul qilasizmi?", default=False)
    onboarding_complete = models.BooleanField(default=False)
    digital_twin_created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username

    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            h = self.height_cm / 100
            return round(self.weight_kg / (h * h), 1)
        return None

    @property
    def risk_score(self):
        score = 20
        if self.glucose_mg_dl:
            if self.glucose_mg_dl >= 180:
                score += 30
            elif self.glucose_mg_dl >= 140:
                score += 18
            elif self.glucose_mg_dl >= 110:
                score += 8
        if self.systolic_bp:
            if self.systolic_bp >= 140:
                score += 15
            elif self.systolic_bp >= 130:
                score += 8
        if self.bmi:
            if self.bmi >= 30:
                score += 12
            elif self.bmi >= 25:
                score += 6
        if self.daily_steps is not None and self.daily_steps < 5000:
            score += 8
        if self.sleep_hours is not None and self.sleep_hours < 6:
            score += 7
        if self.age and self.age >= 50:
            score += 5
        return min(score, 100)

    @property
    def risk_level(self):
        s = self.risk_score
        if s >= 70:
            return "Yuqori"
        if s >= 40:
            return "O'rta"
        return "Past"

    @property
    def risk_factors(self):
        factors = []
        if self.glucose_mg_dl and self.glucose_mg_dl >= 140:
            factors.append({"title": "Glyukoza me'yordan yuqori", "level": "Yuqori", "icon": "droplet", "severity": "high"})
        if self.daily_steps is not None and self.daily_steps < 6000:
            factors.append({"title": "Faollik darajasi past", "level": "O'rta", "icon": "activity", "severity": "medium"})
        if self.sleep_hours is not None and self.sleep_hours < 7:
            factors.append({"title": "Uyqu yetarli emas", "level": "O'rta", "icon": "moon", "severity": "medium"})
        if self.takes_medication:
            factors.append({"title": "Dori qabul qilishda uzilish mavjud", "level": "Yuqori", "icon": "pill", "severity": "high"})
        if not factors:
            factors.append({"title": "Ayni damda jiddiy xavf omillari aniqlanmadi", "level": "Past", "icon": "check", "severity": "low"})
        return factors

    @property
    def affected_organ(self):
        if self.glucose_mg_dl and self.glucose_mg_dl >= 140:
            return "liver"
        if self.systolic_bp and self.systolic_bp >= 135:
            return "heart"
        return "liver"
