from evals.run_eval import run


def test_fictional_evaluation_regression():
    result = run()
    assert result["cases"] == 60
    assert result["category_correct"] >= 54
    assert result["evidence_hits"] >= 30
    assert result["abstentions"] >= 15
    assert result["sensitive_detected"] == result["sensitive_cases"]
