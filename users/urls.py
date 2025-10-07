from django.urls import path

from .views import ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]
