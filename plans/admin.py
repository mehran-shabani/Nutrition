from django.contrib import admin

from .models import PlanItem, WeeklyPlan


class PlanItemInline(admin.TabularInline):
    model = PlanItem
    extra = 0


@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ("user", "start_date", "end_date", "created_at")
    list_filter = ("start_date",)
    search_fields = ("user__username", "notes")
    inlines = [PlanItemInline]


@admin.register(PlanItem)
class PlanItemAdmin(admin.ModelAdmin):
    list_display = ("weekly_plan", "day_of_week", "meal_type", "food", "servings")
    list_filter = ("day_of_week", "meal_type")
    autocomplete_fields = ("weekly_plan", "food")
