from django.db import models
from django.utils.translation import gettext_lazy as _


class Food(models.Model):
    """A simple catalog entry representing macro nutrients per serving."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=120, blank=True)
    serving_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text=_("Default serving size"),
    )
    serving_unit = models.CharField(max_length=32, default=_("g"))
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")

    def __str__(self) -> str:
        return self.name

    @property
    def calories_per_gram(self) -> float:
        if self.serving_size:
            return float(self.calories) / float(self.serving_size)
        return 0.0
