from decimal import Decimal

import pytest
from django.urls import reverse

from plans.plan_engine import generate_weekly_plan
from users.models import Profile


@pytest.mark.django_db
def test_plan_pdf_view_returns_pdf_response(client, profile_factory, food_factory):
    profile = profile_factory(
        weight_kg=Decimal("72"),
        height_cm=Decimal("178"),
        age=28,
        gender=Profile.Gender.MALE,
    )
    user = profile.user
    client.force_login(user)

    for _ in range(8):
        food_factory()

    plan = generate_weekly_plan(profile)
    url = reverse("plans:pdf", args=[plan.pk])

    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert len(response.content) > 0
