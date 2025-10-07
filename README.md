# Nutrition Assistant

یک پروژه جنگو برای مدیریت پروفایل تغذیه، ثبت وعده‌های غذایی و تولید برنامه هفتگی.

## توسعه

پیش‌نیازها را نصب کنید:

```bash
pip install -r requirements.txt
```

برای داشتن داده اولیه بانک غذا، از فیکسچر نمونه استفاده کنید:

```bash
python manage.py loaddata foods/fixtures/foods_min.json
```

سپس می‌توانید سرور توسعه را اجرا کنید:

```bash
python manage.py migrate
python manage.py runserver
```

## تست‌ها و CI

برای اجرای تست‌های خودکار و همان چیزی که در CI استفاده می‌شود، دستور زیر را اجرا کنید:

```bash
pytest
```

این پیکربندی از `pytest-django` استفاده می‌کند و به‌صورت خودکار تنظیمات جنگو و پایگاه‌داده آزمایشی را مقداردهی می‌کند.
