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
