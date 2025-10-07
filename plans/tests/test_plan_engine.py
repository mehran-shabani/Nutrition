from datetime import date
from decimal import Decimal

import pytest

from logs.calorie_math import calculate_tdee
from plans.models import PlanItem
from plans.plan_engine import generate_weekly_plan


@pytest.mark.django_db
def test_generate_weekly_plan_creates_full_week(profile_factory, food_factory):
    profile = profile_factory()
    for _ in range(6):
        food_factory()

    start_date = date(2024, 1, 1)
    plan = generate_weekly_plan(profile, start_date=start_date)

    assert plan.start_date == start_date
    expected_items = len(PlanItem.DayOfWeek.ordered()) * len(PlanItem.MealType.choices)
    assert plan.items.count() == expected_items

    daily_target = calculate_tdee(profile) / len(PlanItem.MealType.choices)
    for item in plan.items.all():
        assert item.total_calories == pytest.approx(daily_target, rel=0.2)
        assert item.servings >= Decimal("0.25")
