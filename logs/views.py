from typing import Any, cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import MealLogForm
from .models import MealLog


class MealLogListView(LoginRequiredMixin, ListView):
    model = MealLog
    template_name = "logs/meal_log_list.html"
    context_object_name = "logs"

    def get_queryset(self) -> QuerySet[MealLog]:
        user = cast(Any, self.request.user)
        return MealLog.objects.filter(user=user).select_related("food")


class MealLogCreateView(LoginRequiredMixin, CreateView):
    model = MealLog
    form_class = MealLogForm
    template_name = "logs/meal_log_form.html"
    success_url = reverse_lazy("logs:list")

    def form_valid(self, form: MealLogForm) -> HttpResponse:
        form.instance.user = cast(Any, self.request.user)
        return super().form_valid(form)
