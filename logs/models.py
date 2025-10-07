from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from foods.models import Food


class MealLog(models.Model):
    """A record of foods eaten by the user."""

    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", _("Breakfast")
        LUNCH = "lunch", _("Lunch")
        DINNER = "dinner", _("Dinner")
        SNACK = "snack", _("Snack")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meal_logs",
    )
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="meal_logs")
    meal_type = models.CharField(max_length=16, choices=MealType.choices)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text=_("Number of servings consumed"),
        default=1,
    )
    consumed_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-consumed_at"]
        verbose_name = _("Meal Log")
        verbose_name_plural = _("Meal Logs")

    def __str__(self) -> str:
        return f"{self.user} - {self.food} ({self.meal_type})"

    @property
    def total_calories(self) -> float:
        return float(self.food.calories) * float(self.quantity)

    @property
    def macros(self) -> dict[str, float]:
        return {
            "protein_g": float(self.food.protein_g) * float(self.quantity),
            "carbs_g": float(self.food.carbs_g) * float(self.quantity),
            "fat_g": float(self.food.fat_g) * float(self.quantity),
        }
