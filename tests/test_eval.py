from evals.run_eval import run


def test_fixed_baseline_cases():
    result = run()
    assert result["cases"] == 4
    assert result["category_correct"] == 4
    assert result["retrieval_correct"] == 4
