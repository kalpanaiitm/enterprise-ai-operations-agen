# Test report

## Verification — 2026-09-28

`python -m pytest -q`: **12 passed locally**. The default evaluation makes no external model calls.

| Measure | 60-case development set | 16-case challenge set |
| --- | ---: | ---: |
| Category accuracy | 60/60 | 16/16 |
| Expected article present, where one applies | 34/34 | 6/6 |
| No article returned, where none applies | 26/26 | 10/10 |
| Sensitive ticket detection recall | 10/10 | 4/4 |

The first implementation returned irrelevant articles on nine development cases. Article scope checks removed those matches. The challenge set then exposed two compromise reports (C13 and C14) receiving generic recovery guidance; an explicit compromise abstention rule removed those matches. Two development labels were also corrected after review: T38 has relevant approved-version guidance, while T44's generic slowness has no relevant crash guidance. Both sets were authored here, inspected and used during development. They are **not blinded, independent performance estimates**. Exact results should not be extrapolated to real tickets. In particular, keyword rules can miss new compromise phrasing, and relevance of a returned article still needs a human reviewer.

The optional OpenAI draft, actual API cost, latency, deployment, and real-world routing are unmeasured. A [prior GitHub Actions run](https://github.com/kalpanaiitm/enterprise-ai-operations-agen/actions/runs/36455663287) passed before the scope refinement. Check Actions for the latest commit's CI result.
