# Test report

## Verified GitHub Actions result

On 2026-09-28, [this workflow run](https://github.com/kalpanaiitm/enterprise-ai-operations-agen/actions/runs/36453221015) completed successfully:

- `python -m pytest -q`: **6 passed in 1.63s**.
- `python -m evals.run_eval`: **category 4/4; retrieval expectations 4/4**.

Tests cover scoped and zero-result retrieval, LangGraph interrupt/resume, approval and rejection, API validation, sensitive classification, duplicate review, and the fixed evaluation cases. All inputs and knowledge articles are original fictional examples; CI makes no model API calls.

## Limits

Four curated cases are a smoke evaluation, not a benchmark of real ticket performance. The optional OpenAI draft, production deployment, latency, cost, and real-world retrieval quality are unmeasured. A green workflow does not establish production readiness.
