from django.urls import path

from .views import (
    WeeklyPlanDetailView,
    WeeklyPlanGenerateView,
    WeeklyPlanPdfView,
    regenerate_current_plan,
)

app_name = "plans"

urlpatterns = [
    path("", WeeklyPlanDetailView.as_view(), name="detail"),
    path("generate/", WeeklyPlanGenerateView.as_view(), name="generate"),
    path("refresh/", regenerate_current_plan, name="refresh"),
    path("pdf/<int:pk>/", WeeklyPlanPdfView.as_view(), name="pdf"),
]
