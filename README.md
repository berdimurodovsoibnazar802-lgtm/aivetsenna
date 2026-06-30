# Alvitsenna — Web platforma (Django)

Mobil ilova prototipi asosida yaratilgan Django web-platforma. Sog'liq ko'rsatkichlari, AI-risk balli (demo statik mantiq) va hologramma uslubidagi 3D Digital Twin (Three.js) bilan.

## Ishga tushirish

```bash
python3 -m venv venv
source venv/bin/activate
pip install django
python3 manage.py migrate
python3 manage.py runserver
```

Demo hisob: `demo` / `demo12345` (yoki "Ro'yxatdan o'tish" orqali yangi hisob yarating).

## Sahifalar

- `/` — Landing
- `/accounts/login/`, `/accounts/register/` — Kirish/ro'yxatdan o'tish
- `/onboarding/` — Boshlang'ich profil yaratish (Digital Twin yaratish)
- `/dashboard/` — Bosh sahifa: AI risk score, kunlik ko'rsatkichlar
- `/twin/` — Digital Twin simulyatori (3D hologramma odam, Three.js)
- `/tahlil/` — AI tahlil: xavf omillari va tavsiya etilgan reja
- `/tavsiyalar/` — Tavsiyalar va reja bajarilishi
- `/profil/` — Profil va sozlamalar

## 3D Digital Twin

`static/js/twin.js` — Three.js orqali jonlantirilgan, erkak/ayol jinsiga qarab proporsiyasi farqlanadigan wireframe inson modeli. Foydalanuvchi ma'lumotlariga qarab (`accounts.models.Profile.affected_organ`) jigar yoki yurak hududida qizil "tashxis" nuqtasi (pulsatsiya bilan) ko'rsatiladi.

## Eslatma

AI tahlil va tavsiyalar hozircha **statik/demo mantiq** asosida ishlaydi (`Profile.risk_score`, `risk_factors` — `accounts/models.py`). Haqiqiy ML modelga ulash uchun shu metodlarni almashtirish kifoya.
