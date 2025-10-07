from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from foods.models import Food


class WeeklyPlan(models.Model):
    """A simple weekly nutrition plan for a profile."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weekly_plans",
    )
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = _("Weekly Plan")
        verbose_name_plural = _("Weekly Plans")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "start_date"],
                name="unique_weekly_plan_per_user_start",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.start_date}"

    @property
    def end_date(self) -> date:
        return self.start_date + timedelta(days=6)

    @property
    def total_calories(self) -> float:
        return sum(item.total_calories for item in self.items.all())


class PlanItem(models.Model):
    """A meal recommendation inside a weekly plan."""

    class DayOfWeek(models.IntegerChoices):
        SATURDAY = 5, _("شنبه")
        SUNDAY = 6, _("یک‌شنبه")
        MONDAY = 0, _("دوشنبه")
        TUESDAY = 1, _("سه‌شنبه")
        WEDNESDAY = 2, _("چهارشنبه")
        THURSDAY = 3, _("پنج‌شنبه")
        FRIDAY = 4, _("جمعه")

        @classmethod
        def ordered(cls) -> list[tuple[int, str]]:
            # Start week on Saturday per Iranian locale
            order = [cls.SATURDAY, cls.SUNDAY, cls.MONDAY, cls.TUESDAY, cls.WEDNESDAY, cls.THURSDAY, cls.FRIDAY]
            return [(choice.value, choice.label) for choice in order]

    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", _("صبحانه")
        LUNCH = "lunch", _("ناهار")
        DINNER = "dinner", _("شام")
        SNACK = "snack", _("میان‌وعده")

    weekly_plan = models.ForeignKey(
        WeeklyPlan,
        on_delete=models.CASCADE,
        related_name="items",
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    meal_type = models.CharField(max_length=16, choices=MealType.choices)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    servings = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _("Plan Item")
        verbose_name_plural = _("Plan Items")
        ordering = ["day_of_week", "meal_type"]
        constraints = [
            models.UniqueConstraint(
                fields=["weekly_plan", "day_of_week", "meal_type"],
                name="unique_plan_item_per_day_meal",
            )
        ]

    def __str__(self) -> str:
        return f"{self.get_day_of_week_display()} {self.get_meal_type_display()}"

    @property
    def total_calories(self) -> float:
        return float(self.food.calories) * float(self.servings)

    @property
    def macros(self) -> dict[str, float]:
        return {
            "protein_g": float(self.food.protein_g) * float(self.servings),
            "carbs_g": float(self.food.carbs_g) * float(self.servings),
            "fat_g": float(self.food.fat_g) * float(self.servings),
        }
