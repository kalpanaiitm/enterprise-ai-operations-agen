# Test report

## Automated workflow

On 2026-09-28, the first GitHub Actions run passed **5 tests** for scoped retrieval, zero matches, LangGraph interrupt/resume, approval, rejection, input validation, sensitive classification and duplicate review. [See that run](https://github.com/kalpanaiitm/enterprise-ai-operations-agen/actions/runs/36453004669).

The fixed `evals/cases.json` set now contains four fictional ticket/category/retrieval expectations. Its results are pending the next workflow run. This small set is a reproducible smoke evaluation, not a measure of performance on real support tickets.

The optional OpenAI route, deployed environment, latency, cost, and real-world retrieval quality remain unevaluated. A green workflow does not establish production readiness.
