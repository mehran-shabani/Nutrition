from django.contrib import admin

from .models import MealLog


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "food",
        "meal_type",
        "quantity",
        "consumed_at",
    )
    list_filter = ("meal_type", "consumed_at")
    autocomplete_fields = ("food", "user")
    search_fields = ("user__username", "food__name")
