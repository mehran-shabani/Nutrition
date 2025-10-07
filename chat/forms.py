from django import forms


class ChatMessageForm(forms.Form):
    message = forms.CharField(
        label="پیام شما",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "سوال خود را درباره تغذیه بپرسید...",
            }
        ),
    )
