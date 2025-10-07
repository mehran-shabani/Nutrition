from django.urls import path

from .views import MealLogCreateView, MealLogListView

app_name = "logs"

urlpatterns = [
    path("", MealLogListView.as_view(), name="list"),
    path("new/", MealLogCreateView.as_view(), name="create"),
]
