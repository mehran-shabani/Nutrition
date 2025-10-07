import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_chat_onboarding_flow_collects_history(client):
    url = reverse("chat:home")

    get_response = client.get(url)
    assert get_response.status_code == 200
    assert get_response.context["history"] == []

    client.post(url, {"message": "سن من 30 است"})
    client.post(url, {"message": "قد من 175 است"})

    session_history = client.session.get("chat_history")

    assert len(session_history) == 2
    assert session_history[0]["user"] == "سن من 30 است"
    assert session_history[1]["user"] == "قد من 175 است"
    assert all(entry["bot"] for entry in session_history)
