from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, TemplateView

from logs.calorie_math import macro_targets_for_profile
from users.models import Profile

from .forms import PlanDateForm
from .models import PlanItem, WeeklyPlan
from .pdf import render_plan_pdf
from .plan_engine import generate_weekly_plan

if TYPE_CHECKING:
    from django.http import HttpRequest


class WeeklyPlanMixin(LoginRequiredMixin):
    if TYPE_CHECKING:
        request: "HttpRequest"

    def get_profile(self) -> Profile:
        user = cast(Any, self.request.user)
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile


class WeeklyPlanDetailView(WeeklyPlanMixin, TemplateView):
    template_name = "plans/weekly_plan_detail.html"

    def get_plan(self) -> WeeklyPlan | None:
        start_date_str = self.request.GET.get("start")
        user = cast(Any, self.request.user)
        queryset: QuerySet[WeeklyPlan] = WeeklyPlan.objects.filter(user=user)
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                return queryset.filter(start_date=start_date).first()
            except ValueError:
                pass
        return queryset.order_by("-start_date").first()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        plan = self.get_plan()
        profile = self.get_profile()
        context["plan"] = plan
        context["profile"] = profile
        context["macro_targets"] = macro_targets_for_profile(profile)
        context["form"] = PlanDateForm(initial={"start_date": timezone.localdate()})
        context["meal_choices"] = []
        if plan:
            day_rows = []
            meal_keys = [meal for meal, _ in plan.items.model.MealType.choices]
            for day_value, day_label in plan.items.model.DayOfWeek.ordered():
                items_map: dict[str, PlanItem | None] = {
                    key: None for key in meal_keys
                }
                for item in (
                    plan.items.filter(day_of_week=day_value)
                    .select_related("food")
                ):
                    items_map[item.meal_type] = item
                ordered_items = [items_map[key] for key in meal_keys]
                day_rows.append({"label": day_label, "items": ordered_items})
            context["day_rows"] = day_rows
            context["meal_choices"] = [
                (key, label) for key, label in plan.items.model.MealType.choices
            ]
        return context


class WeeklyPlanGenerateView(WeeklyPlanMixin, FormView):
    template_name = "plans/weekly_plan_generate.html"
    form_class = PlanDateForm
    success_url = reverse_lazy("plans:detail")

    def form_valid(self, form: PlanDateForm) -> HttpResponse:
        profile = self.get_profile()
        start_date = form.cleaned_data["start_date"]
        try:
            generate_weekly_plan(profile, start_date)
            messages.success(self.request, "برنامه غذایی جدید ایجاد شد.")
        except ValueError as exc:
            messages.error(self.request, str(exc))
        return super().form_valid(form)


class WeeklyPlanPdfView(WeeklyPlanMixin, DetailView):
    model = WeeklyPlan

    def get_object(
        self,
        queryset: QuerySet[WeeklyPlan] | None = None,
    ) -> WeeklyPlan:
        plan = cast(WeeklyPlan, super().get_object(queryset))
        if plan.user != self.request.user:
            raise PermissionDenied("Access denied")
        return plan

    def get(
        self,
        request: "HttpRequest",
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        plan = self.get_object()
        pdf_bytes = render_plan_pdf(plan)
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = (
            f"attachment; filename=plan-{plan.start_date}.pdf"
        )
        return response


def regenerate_current_plan(request: "HttpRequest") -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    user = cast(Any, request.user)
    profile, _ = Profile.objects.get_or_create(user=user)
    start_date = timezone.localdate()
    try:
        generate_weekly_plan(profile, start_date)
        messages.success(request, "برنامه هفته جاری به‌روزرسانی شد.")
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect("plans:detail")
