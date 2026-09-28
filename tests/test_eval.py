from evals.run_eval import run
from evals.run_product_eval import run as run_product
from pathlib import Path


def test_fictional_evaluation_regression():
    result = run()
    assert result["cases"] == 60
    assert result["category_correct"] >= 54
    assert result["evidence_hits"] >= 32
    assert result["abstentions"] >= 24
    assert result["sensitive_detected"] == result["sensitive_cases"]


def test_separate_challenge_cases():
    result = run(Path(__file__).resolve().parent.parent / "evals" / "challenge_cases.json")
    assert result["cases"] == 16
    assert result["evidence_hits"] >= 5
    assert result["abstentions"] >= 9
    assert result["sensitive_detected"] == result["sensitive_cases"]


def test_offline_product_decisions(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = run_product()
    assert result["cases"] == 14
    assert result["escalation_ok"] >= 13
    assert result["source_ok"] >= 13
    assert result["draft_ok"] >= 13
    assert result["review_paused"] == result["cases"]
