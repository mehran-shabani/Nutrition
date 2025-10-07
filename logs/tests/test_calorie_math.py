from collections.abc import Callable
from decimal import Decimal

import pytest

from logs.calorie_math import calculate_bmr, calculate_tdee
from users.models import Profile


def test_calculate_bmr_mifflin_st_jeor(
    profile_factory: Callable[..., Profile],
) -> None:
    profile = profile_factory(
        weight_kg=Decimal("70"),
        height_cm=Decimal("175"),
        age=30,
        gender=Profile.Gender.MALE,
    )

    bmr = calculate_bmr(profile)

    assert bmr == pytest.approx(1648.75, rel=1e-3)


@pytest.mark.parametrize(
    "activity, goal, expected",
    [
        (Profile.ActivityLevel.SEDENTARY, Profile.Goal.MAINTAIN, 1978.5),
        (Profile.ActivityLevel.MODERATE, Profile.Goal.GAIN, 2811.11875),
    ],
)
def test_calculate_tdee_with_activity_and_goal(
    profile_factory: Callable[..., Profile],
    activity: str,
    goal: str,
    expected: float,
) -> None:
    profile = profile_factory(
        weight_kg=Decimal("70"),
        height_cm=Decimal("175"),
        age=30,
        gender=Profile.Gender.MALE,
        activity_level=activity,
        goal=goal,
    )

    tdee = calculate_tdee(profile)

    assert tdee == pytest.approx(expected, rel=1e-3)
