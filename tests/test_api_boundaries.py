"""API boundary tests for the fictional support-agent demo.

These tests exercise validation and failure paths without calling an LLM.
The demo intentionally has no authentication and must not accept real tickets.
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from support_agent.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("text", ["", "short", "x" * 2001])
def test_ticket_rejects_invalid_text_length(text):
    response = client.post("/tickets", json={"text": text})
    assert response.status_code == 422


def test_ticket_rejects_missing_text():
    response = client.post("/tickets", json={})
    assert response.status_code == 422


def test_lookup_rejects_malformed_ticket_identifier():
    response = client.get("/tickets/not-a-uuid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_lookup_returns_404_for_unknown_valid_identifier():
    response = client.get(f"/tickets/{uuid4()}")
    assert response.status_code == 404


def test_review_rejects_blank_edited_response_without_resuming(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    created = client.post("/tickets", json={"text": "My VPN connection is failing"})
    assert created.status_code == 201
    ticket_id = created.json()["ticket_id"]

    invalid = client.post(
        f"/tickets/{ticket_id}/review",
        json={"approved": True, "edited_response": "   "},
    )
    assert invalid.status_code == 422
    assert client.get(f"/tickets/{ticket_id}").json()["status"] == "pending_review"


def test_review_rejects_invalid_approval_type_without_resuming(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    created = client.post("/tickets", json={"text": "My VPN connection is failing"})
    assert created.status_code == 201
    ticket_id = created.json()["ticket_id"]

    invalid = client.post(
        f"/tickets/{ticket_id}/review",
        json={"approved": "definitely", "edited_response": "Reviewed."},
    )
    assert invalid.status_code == 422
    assert client.get(f"/tickets/{ticket_id}").json()["status"] == "pending_review"
