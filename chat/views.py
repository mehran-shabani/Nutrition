from typing import Any, cast

from django.http import HttpResponse
from django.views.generic import FormView

from .forms import ChatMessageForm


class ChatView(FormView):
    template_name = "chat/chat.html"
    form_class = ChatMessageForm

    def get_initial(self) -> dict[str, str]:
        return {"message": ""}

    def get_history(self) -> list[dict[str, str]]:
        history = cast(
            list[dict[str, str]],
            self.request.session.get("chat_history", []),
        )
        return history

    def store_history(self, history: list[dict[str, str]]) -> None:
        self.request.session["chat_history"] = history
        self.request.session.modified = True

    def generate_response(self, user_message: str) -> str:
        # Placeholder heuristic response
        return "برای پاسخ دقیق‌تر به متخصص تغذیه مراجعه کنید. این یک ربات نمایشی است."  # noqa: E501

    def form_valid(self, form: ChatMessageForm) -> HttpResponse:
        history = self.get_history()
        user_message = form.cleaned_data["message"].strip()
        if user_message:
            history.append(
                {
                    "user": user_message,
                    "bot": self.generate_response(user_message),
                }
            )
            self.store_history(history)
        return self.render_to_response(self.get_context_data(form=self.form_class()))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["history"] = self.get_history()
        return context
