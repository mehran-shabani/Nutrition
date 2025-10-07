from django import forms

from .models import PlanItem


class PlanDateForm(forms.Form):
    start_date = forms.DateField(
        label="شروع هفته",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )


class PlanItemForm(forms.ModelForm):
    class Meta:
        model = PlanItem
        fields = ["day_of_week", "meal_type", "food", "servings", "notes"]
        widgets = {
            "day_of_week": forms.Select(attrs={"class": "form-select"}),
            "meal_type": forms.Select(attrs={"class": "form-select"}),
            "food": forms.Select(attrs={"class": "form-select"}),
            "servings": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.25", "min": 0.25}
            ),
            "notes": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "day_of_week": "روز هفته",
            "meal_type": "وعده",
            "food": "غذا",
            "servings": "تعداد سهم",
            "notes": "یادداشت",
        }
