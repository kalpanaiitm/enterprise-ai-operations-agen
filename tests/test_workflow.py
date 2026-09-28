from langgraph.types import Command

from support_agent.knowledge import search
from support_agent.workflow import create_graph


def test_retrieval_is_scoped_and_zero_matches_are_not_evidence():
    assert search("vpn connection", "network")[0]["id"] == "KB-NETWORK-01"
    assert search("vpn connection", "account") == []
    assert search("galactic banana", "network") == []


def test_graph_interrupts_and_resumes_after_human_approval(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    graph = create_graph()
    config = {"configurable": {"thread_id": "test-1"}}
    result = graph.invoke({"ticket": "My VPN connection is failing"}, config)
    assert result["__interrupt__"]
    assert graph.get_state(config).next == ("review",)
    assert result["evidence"][0]["id"] == "KB-NETWORK-01"
    final = graph.invoke(Command(resume={"approved": True, "edited_response": "Reviewed guidance."}), config)
    assert final["status"] == "approved"
    assert final["final_response"] == "Reviewed guidance."
    assert not graph.get_state(config).next


def test_unknown_ticket_still_requires_review(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    graph = create_graph()
    config = {"configurable": {"thread_id": "test-2"}}
    result = graph.invoke({"ticket": "Galactic banana problem"}, config)
    assert result["evidence"] == []
    assert result["__interrupt__"]
    final = graph.invoke(Command(resume={"approved": False}), config)
    assert final["status"] == "rejected"
    assert final["final_response"] == ""
