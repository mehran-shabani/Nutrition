from __future__ import annotations

from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from itertools import cycle

from django.db import transaction
from django.utils import timezone

from foods.models import Food
from logs.calorie_math import calculate_tdee
from users.models import Profile

from .models import PlanItem, WeeklyPlan


def _servings_for_target(food: Food, daily_calories: float) -> Decimal:
    meals_per_day = len(PlanItem.MealType.choices)
    calories_per_meal = daily_calories / meals_per_day
    if float(food.calories) <= 0:
        return Decimal("1")
    servings = Decimal(calories_per_meal) / Decimal(food.calories)
    servings = servings.quantize(Decimal("0.25"), rounding=ROUND_HALF_UP)
    return max(servings, Decimal("0.25"))


@transaction.atomic
def generate_weekly_plan(
    profile: Profile,
    start_date: date | None = None,
) -> WeeklyPlan:
    """Create or refresh a weekly plan for the given profile."""

    if start_date is None:
        start_date = timezone.localdate()

    foods = list(Food.objects.filter(is_public=True).order_by("name"))
    if not foods:
        raise ValueError("No foods available to build a plan. Load fixtures first.")

    plan, _ = WeeklyPlan.objects.get_or_create(
        user=profile.user,
        start_date=start_date,
        defaults={"notes": ""},
    )
    plan.items.all().delete()

    daily_calories = calculate_tdee(profile) or 2000
    food_cycle = cycle(foods)

    for index, (day_value, _) in enumerate(PlanItem.DayOfWeek.ordered()):
        # Align to actual calendar date to support PDF export contexts
        day_date = start_date + timedelta(days=index)
        for meal_value, _ in PlanItem.MealType.choices:
            food = next(food_cycle)
            servings = _servings_for_target(food, daily_calories)
            PlanItem.objects.create(
                weekly_plan=plan,
                day_of_week=day_value,
                meal_type=meal_value,
                food=food,
                servings=servings,
                notes=f"پیشنهاد برای {day_date.strftime('%Y-%m-%d')}",
            )

    return plan
