# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential pkg-config libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN addgroup --system app \
    && adduser --system --ingroup app --home /app app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY manage.py ./
COPY nutrition_bot/ ./nutrition_bot/
COPY chat/ ./chat/
COPY foods/ ./foods/
COPY logs/ ./logs/
COPY plans/ ./plans/
COPY templates/ ./templates/
COPY users/ ./users/
COPY static/ ./static/

RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "nutrition_bot.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
