# Test report

## Verified GitHub Actions result

On 2026-09-28, [this workflow run](https://github.com/kalpanaiitm/enterprise-ai-operations-agen/actions/runs/36454085091) completed successfully:

- `python -m pytest -q`: **10 tests passed**.
- `python -m evals.run_eval`: **category 4/4; retrieval expectations 4/4**.

The suite covers scoped and zero-result retrieval, LangGraph interrupt/resume, approval and rejection, API validation, sensitive classification, duplicate review, mocked model success, unsafe model output fallback, sensitive-ticket model bypass and provider failure. All tickets and knowledge articles are original fictional examples. Tests make no paid model calls.

## Limits

The four curated evaluation cases are a smoke check, not a benchmark of real support tickets. The optional OpenAI route is tested with mocks, not a real provider call. Deployed behaviour, latency, actual API cost and real-world retrieval quality remain unmeasured. A green workflow does not establish production readiness.
