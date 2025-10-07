from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from itertools import count
from typing import Any, cast

import pytest
from django.contrib.auth.models import AbstractBaseUser

from foods.models import Food
from users.models import Profile


@pytest.fixture
def user_factory(
    django_user_model: Any,
) -> Callable[..., AbstractBaseUser]:
    sequence = count(1)

    def factory(**kwargs: Any) -> AbstractBaseUser:
        index = next(sequence)
        username = kwargs.pop("username", f"user{index}")
        email = kwargs.pop("email", f"user{index}@example.com")
        password = kwargs.pop("password", "testpass123")
        user = cast(
            AbstractBaseUser,
            django_user_model.objects.create_user(
                username=username,
                email=email,
                password=password,
                **kwargs,
            ),
        )
        return user

    return factory


@pytest.fixture
def profile_factory(
    user_factory: Callable[..., AbstractBaseUser],
) -> Callable[..., Profile]:
    def factory(**kwargs: Any) -> Profile:
        user = kwargs.pop("user", None) or user_factory()
        defaults = {
            "age": 30,
            "height_cm": Decimal("175"),
            "weight_kg": Decimal("70"),
            "gender": Profile.Gender.MALE,
            "activity_level": Profile.ActivityLevel.MODERATE,
            "goal": Profile.Goal.MAINTAIN,
        }
        defaults.update(kwargs)
        profile, _ = Profile.objects.update_or_create(user=user, defaults=defaults)
        return profile

    return factory


@pytest.fixture
def food_factory() -> Callable[..., Food]:
    sequence = count(1)

    def factory(**kwargs: Any) -> Food:
        index = next(sequence)
        defaults = {
            "name": f"Test Food {index}",
            "description": "",
            "serving_size": Decimal("100"),
            "serving_unit": "g",
            "calories": Decimal("400"),
            "protein_g": Decimal("30"),
            "carbs_g": Decimal("40"),
            "fat_g": Decimal("10"),
            "is_public": True,
        }
        defaults.update(kwargs)
        return Food.objects.create(**defaults)

    return factory
