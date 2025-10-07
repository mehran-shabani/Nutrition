from __future__ import annotations

import os
from io import BytesIO
from typing import Any

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template

from xhtml2pdf import pisa


def _link_callback(uri: str, rel: str) -> str:
    result = finders.find(uri)
    if result:
        if isinstance(result, (list, tuple)):
            result = result[0]
        return result

    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        if os.path.exists(path):
            return path

    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT or "", uri.replace(settings.STATIC_URL, ""))
        if os.path.exists(path):
            return path

    return uri


def render_plan_pdf(weekly_plan, context: dict[str, Any] | None = None, template_name: str = "plans/plan_pdf.html") -> bytes:
    template = get_template(template_name)
    items = list(weekly_plan.items.select_related("food").all())
    day_choices = weekly_plan.items.model.DayOfWeek.ordered()
    meal_choices = weekly_plan.items.model.MealType.choices
    meal_keys = [value for value, _ in meal_choices]

    items_by_day: dict[int, dict[str, Any]] = {}
    for item in items:
        items_by_day.setdefault(item.day_of_week, {})[item.meal_type] = item

    day_rows = []
    for day_value, day_label in day_choices:
        day_map = items_by_day.get(day_value, {})
        ordered_items = [day_map.get(meal_key) for meal_key in meal_keys]
        day_rows.append({"label": day_label, "items": ordered_items})

    base_context = {
        "plan": weekly_plan,
        "items": items,
        "day_choices": day_choices,
        "meal_choices": meal_choices,
        "day_rows": day_rows,
    }
    if context:
        base_context.update(context)

    html = template.render(base_context)
    output = BytesIO()
    pdf_status = pisa.CreatePDF(html, dest=output, encoding="utf-8", link_callback=_link_callback)
    if pdf_status.err:
        raise ValueError("Failed to render PDF")
    return output.getvalue()
