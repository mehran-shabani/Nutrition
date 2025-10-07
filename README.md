# Nutrition Assistant

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
[![Build & Publish Image](https://github.com/OWNER/REPO/actions/workflows/build.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/build.yml)
[![Release Please](https://github.com/OWNER/REPO/actions/workflows/release-please.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/release-please.yml)

یک پروژه جنگو برای مدیریت پروفایل تغذیه، ثبت وعده‌های غذایی و تولید برنامه هفتگی.

## توسعه

پیش‌نیازها را نصب کنید:

```bash
pip install -r requirements.txt
```

برای ابزارهای توسعه (lint، تایپ‌چک و تست با کاورج) فایل dev را نیز نصب کنید:

```bash
pip install -r requirements-dev.txt
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

## گردش‌کار CI/CD

- فایل‌های workflow در پوشه `.github/workflows/` قرار دارند و با برنچ `main` و Pull Requestها اجرا می‌شوند.
- CI شامل `ruff`، `mypy` و `pytest` (به همراه گزارش کاورج) روی نسخه‌های ۳٫۱۱ و ۳٫۱۲ پایتون است.
- هر بار push به `main` یا تگ‌های نسخه (`vMAJOR.MINOR.PATCH`) باعث ساخت ایمیج Docker و انتشار آن در GHCR می‌شود.
- انتشار Release با استفاده از [Release Please](https://github.com/googleapis/release-please) انجام می‌شود؛ پیام کمیت‌ها باید بر اساس الگوی Conventional Commits باشند.
- نکته: مقادیر placeholder مانند `OWNER/REPO` یا `org/team` را در پیکربندی‌ها با مقادیر واقعی پروژه جایگزین کنید.

### قطع نسخه و انتشار

۱. کمیت‌ها را با الگوی Conventional Commits بنویسید (`feat: ...`, `fix: ...`، و غیره).
۲. پس از merge در `main`، Release Please به صورت خودکار Pull Request نسخه بعدی و `CHANGELOG.md` را می‌سازد.
۳. با merge شدن PR انتشار، تگ `vMAJOR.MINOR.PATCH` ایجاد و Release در GitHub منتشر می‌شود.

### ساخت و مصرف ایمیج Docker

ایمیج‌ها در [GitHub Container Registry](https://ghcr.io) با نام `ghcr.io/OWNER/REPO` منتشر می‌شوند (جایگزین کردن `OWNER/REPO` با نام واقعی).

برای کشیدن آخرین نسخه پایدار:

```bash
docker pull ghcr.io/OWNER/REPO:v1.0.0
```

برای اجرای محلی با docker compose از `compose.deploy.yml` استفاده کنید و متغیر `IMAGE_REF` را مشخص کنید:

```bash
IMAGE_REF=ghcr.io/OWNER/REPO:v1.0.0 docker compose -f compose.deploy.yml up -d
```

### پیکربندی استقرار (CD)

استقرار پس از انتشار Release و تنها در صورت وجود Secrets زیر فعال می‌شود:

- `DEPLOY_HOST`: آدرس سرور مقصد
- `DEPLOY_USER`: کاربر SSH روی سرور
- `DEPLOY_KEY`: کلید خصوصی SSH با دسترسی به کاربر فوق
- `DEPLOY_PATH`: مسیر روی سرور برای قرار گرفتن فایل‌های استقرار
- `ENV_FILE`: (اختیاری) محتوای فایل `.env` جهت بارگذاری روی سرور
- `GHCR_TOKEN`: (اختیاری) توکن با دسترسی `read:packages` در صورت خصوصی بودن ایمیج‌ها
- `GHCR_USERNAME`: (اختیاری) نام کاربری مرتبط با توکن GHCR؛ در صورت عدم تنظیم، از `OWNER` استفاده می‌شود

Workflow به شکل زیر عمل می‌کند:

1. فایل‌های `compose.deploy.yml` و `.env` را روی سرور بارگذاری می‌کند.
2. ایمیج مربوط به تگ Release را از GHCR می‌کشد.
3. سرویس را با `docker compose up -d` اجرا کرده و سپس دستورات `migrate` و `collectstatic` را اجرا می‌کند.

در صورت عدم تنظیم Secrets، Job مربوط به استقرار به طور خودکار Skip می‌شود.

## توسعه با Docker

برای ساخت ایمیج محلی:

```bash
docker build -t nutrition-assistant:local .
docker run --rm -p 8000:8000 nutrition-assistant:local
```

این ایمیج از `gunicorn` برای سرویس‌دهی استفاده می‌کند.
