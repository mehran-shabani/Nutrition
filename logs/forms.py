from typing import Any, cast

from django import forms

from foods.models import Food

from .models import MealLog


class MealLogForm(forms.ModelForm):
    food = forms.ModelChoiceField(
        queryset=Food.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="غذا",
    )

    class Meta:
        model = MealLog
        fields = ["food", "meal_type", "quantity", "consumed_at", "notes"]
        widgets = {
            "meal_type": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.25", "min": 0.25}
            ),
            "consumed_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
        labels = {
            "meal_type": "وعده",
            "quantity": "تعداد سهم",
            "consumed_at": "زمان مصرف",
            "notes": "یادداشت",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        food_field = cast(
            forms.ModelChoiceField,
            self.fields["food"],
        )
        food_field.queryset = Food.objects.filter(is_public=True)
