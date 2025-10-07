from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import MealLogForm
from .models import MealLog


class MealLogListView(LoginRequiredMixin, ListView):
    model = MealLog
    template_name = "logs/meal_log_list.html"
    context_object_name = "logs"

    def get_queryset(self):
        return MealLog.objects.filter(user=self.request.user).select_related("food")


class MealLogCreateView(LoginRequiredMixin, CreateView):
    model = MealLog
    form_class = MealLogForm
    template_name = "logs/meal_log_form.html"
    success_url = reverse_lazy("logs:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
