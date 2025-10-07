from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class HealthCondition(models.Model):
    """Medical or dietary constraints a user wants to track."""

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Health Condition")
        verbose_name_plural = _("Health Conditions")

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    """Additional nutrition related attributes for a user."""

    class Gender(models.TextChoices):
        FEMALE = "F", _("Female")
        MALE = "M", _("Male")
        OTHER = "O", _("Other")

    class ActivityLevel(models.TextChoices):
        SEDENTARY = "SED", _("Sedentary (office job)")
        LIGHT = "LGT", _("Lightly active")
        MODERATE = "MOD", _("Moderately active")
        ACTIVE = "ACT", _("Very active")
        ATHLETE = "ATH", _("Athlete")

    class Goal(models.TextChoices):
        LOSE = "LOSE", _("Fat loss")
        MAINTAIN = "MAINTAIN", _("Maintain weight")
        GAIN = "GAIN", _("Gain muscle/weight")

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="profile",
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Height in centimeters"),
    )
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Weight in kilograms"),
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
    )
    activity_level = models.CharField(
        max_length=3,
        choices=ActivityLevel.choices,
        default=ActivityLevel.SEDENTARY,
    )
    goal = models.CharField(
        max_length=8,
        choices=Goal.choices,
        default=Goal.MAINTAIN,
    )
    dietary_preferences = models.TextField(blank=True)
    health_conditions = models.ManyToManyField(
        HealthCondition,
        blank=True,
        related_name="profiles",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self) -> str:
        return f"{self.user.get_username()} profile"
