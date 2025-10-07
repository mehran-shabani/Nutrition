from typing import Any, cast

from django import forms

from .models import HealthCondition, Profile


class ProfileForm(forms.ModelForm):
    health_conditions = forms.ModelMultipleChoiceField(
        queryset=HealthCondition.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="شرایط پزشکی",
    )

    class Meta:
        model = Profile
        fields = [
            "age",
            "height_cm",
            "weight_kg",
            "gender",
            "activity_level",
            "goal",
            "dietary_preferences",
            "health_conditions",
        ]
        widgets = {
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "height_cm": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1", "min": 0}
            ),
            "weight_kg": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1", "min": 0}
            ),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "activity_level": forms.Select(attrs={"class": "form-select"}),
            "goal": forms.Select(attrs={"class": "form-select"}),
            "dietary_preferences": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }
        labels = {
            "age": "سن",
            "height_cm": "قد (سانتی‌متر)",
            "weight_kg": "وزن (کیلوگرم)",
            "gender": "جنسیت",
            "activity_level": "میزان فعالیت",
            "goal": "هدف",
            "dietary_preferences": "علایق غذایی",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        health_field = cast(
            forms.ModelMultipleChoiceField,
            self.fields["health_conditions"],
        )
        health_field.queryset = HealthCondition.objects.all()


class HealthConditionForm(forms.ModelForm):
    class Meta:
        model = HealthCondition
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
        labels = {
            "name": "عنوان",
            "description": "توضیحات",
        }
