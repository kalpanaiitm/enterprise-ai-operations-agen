# Test report

Automated checks cover scoped retrieval, zero matches, LangGraph interrupt/resume, approval, rejection, input validation, sensitive classification, and duplicate review. CI uses the deterministic default and makes no paid API calls.

**Status:** tests are committed; GitHub Actions must run before a PASS is recorded. The optional OpenAI route, deployment, latency, and retrieval quality are not yet evaluated. A green workflow does not establish production readiness.
