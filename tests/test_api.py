from fastapi.testclient import TestClient
from support_agent.api import app

client = TestClient(app)


def test_ticket_review_is_explicit_and_not_sent(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    created = client.post("/tickets", json={"text": "My VPN connection is failing"})
    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "pending_review"
    assert body["evidence"][0]["id"] == "KB-NETWORK-01"
    ticket_id = body["ticket_id"]
    assert client.get(f"/tickets/{ticket_id}").json()["status"] == "pending_review"
    approved = client.post(f"/tickets/{ticket_id}/review", json={"approved": True, "edited_response": "Reviewed."})
    assert approved.status_code == 200
    assert approved.json()["final_response"] == "Reviewed."
    assert client.post(f"/tickets/{ticket_id}/review", json={"approved": True}).status_code == 409


def test_validation_and_sensitive_routing(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    assert client.post("/tickets", json={"text": "short"}).status_code == 422
    body = client.post("/tickets", json={"text": "I suspect a phishing login message"}).json()
    assert body["sensitive"] is True
    assert body["status"] == "pending_review"
