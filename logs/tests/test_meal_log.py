from collections.abc import Callable
from decimal import Decimal

import pytest

from foods.models import Food
from logs.models import MealLog
from users.models import Profile


@pytest.mark.django_db
def test_meal_log_macro_totals(
    profile_factory: Callable[..., Profile],
    food_factory: Callable[..., Food],
) -> None:
    profile = profile_factory()
    food = food_factory(
        calories=Decimal("250"),
        protein_g=Decimal("15"),
        carbs_g=Decimal("20"),
        fat_g=Decimal("8"),
    )

    log = MealLog.objects.create(
        user=profile.user,
        food=food,
        meal_type=MealLog.MealType.BREAKFAST,
        quantity=Decimal("2.5"),
    )

    macros = log.macros

    assert macros["protein_g"] == pytest.approx(37.5)
    assert macros["carbs_g"] == pytest.approx(50)
    assert macros["fat_g"] == pytest.approx(20)
    assert log.total_calories == pytest.approx(625)
