from django.urls import path

from .views import FoodAutocompleteView, FoodListView

app_name = "foods"

urlpatterns = [
    path("", FoodListView.as_view(), name="list"),
    path("autocomplete/", FoodAutocompleteView.as_view(), name="autocomplete"),
]
