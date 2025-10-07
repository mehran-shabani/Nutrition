from django.contrib import admin

from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "serving_size",
        "serving_unit",
        "calories",
        "protein_g",
        "carbs_g",
        "fat_g",
        "is_public",
    )
    list_filter = ("is_public",)
    search_fields = ("name", "brand")
