from django.contrib import admin

from .models import HealthCondition, Profile


@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "age",
        "height_cm",
        "weight_kg",
        "activity_level",
        "goal",
        "updated_at",
    )
    list_filter = ("activity_level", "goal", "gender")
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("health_conditions",)
