from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from users.models import Profile


ACTIVITY_MULTIPLIERS: Dict[str, float] = {
    Profile.ActivityLevel.SEDENTARY: 1.2,
    Profile.ActivityLevel.LIGHT: 1.375,
    Profile.ActivityLevel.MODERATE: 1.55,
    Profile.ActivityLevel.ACTIVE: 1.725,
    Profile.ActivityLevel.ATHLETE: 1.9,
}

GOAL_MODIFIERS: Dict[str, float] = {
    Profile.Goal.LOSE: 0.85,
    Profile.Goal.MAINTAIN: 1.0,
    Profile.Goal.GAIN: 1.1,
}


def _to_decimal(value) -> Decimal:
    if value in (None, ""):
        return Decimal(0)
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def calculate_bmr(profile: Profile) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor."""

    weight = _to_decimal(profile.weight_kg)
    height = _to_decimal(profile.height_cm)
    age = _to_decimal(profile.age)
    if not weight or not height or not age:
        return 0.0

    base = (10 * weight) + (6.25 * height) - (5 * age)
    if profile.gender == Profile.Gender.MALE:
        base += 5
    else:
        base -= 161
    return float(base)


def calculate_tdee(profile: Profile) -> float:
    """Estimate total daily energy expenditure (TDEE)."""

    bmr = calculate_bmr(profile)
    if bmr <= 0:
        # Provide a sensible default when information is incomplete
        bmr = 1500

    activity_multiplier = ACTIVITY_MULTIPLIERS.get(profile.activity_level, 1.2)
    goal_multiplier = GOAL_MODIFIERS.get(profile.goal, 1.0)
    return float(bmr * activity_multiplier * goal_multiplier)


def distribute_macros(calories: float, profile: Profile | None = None) -> dict[str, float]:
    """Return target macro distribution (grams) for a given calorie intake."""

    if calories <= 0:
        calories = 2000

    if profile and profile.goal == Profile.Goal.GAIN:
        ratios = {"protein": 0.25, "carbs": 0.5, "fat": 0.25}
    elif profile and profile.goal == Profile.Goal.LOSE:
        ratios = {"protein": 0.35, "carbs": 0.35, "fat": 0.30}
    else:
        ratios = {"protein": 0.30, "carbs": 0.45, "fat": 0.25}

    protein_calories = calories * ratios["protein"]
    carb_calories = calories * ratios["carbs"]
    fat_calories = calories * ratios["fat"]

    return {
        "protein_g": protein_calories / 4,
        "carbs_g": carb_calories / 4,
        "fat_g": fat_calories / 9,
    }


@dataclass
class MacroTargets:
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


def macro_targets_for_profile(profile: Profile) -> MacroTargets:
    calories = calculate_tdee(profile)
    macros = distribute_macros(calories, profile)
    return MacroTargets(calories=calories, **macros)
