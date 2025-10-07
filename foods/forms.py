from django import forms


class FoodSearchForm(forms.Form):
    query = forms.CharField(
        label="جستجوی غذا",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام غذا یا برند...",
                "autocomplete": "off",
            }
        ),
    )
