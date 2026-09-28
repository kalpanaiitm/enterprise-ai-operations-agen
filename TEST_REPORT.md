# Test report

## Verification — 2026-09-28

`python -m pytest -q`: **13 passed locally**. Both evaluation commands make no external model calls when model variables are unset.

| Measure | 60-case development set | 16-case challenge set |
| --- | ---: | ---: |
| Category accuracy | 60/60 | 16/16 |
| Expected article present, where one applies | 34/34 | 6/6 |
| No article returned, where none applies | 26/26 | 10/10 |
| Sensitive ticket detection recall | 10/10 | 4/4 |

A separate 14-case offline workflow evaluation measures escalation 14/14, source choice 14/14, draft checks 14/14, review pause 14/14, and deterministic mode 14/14. Its draft check validates an expected excerpt and exact source ID plus a narrow unsupported-action phrase check. It does **not** judge tone, factual entailment, or model-generated text. The escalation labels are authored policy expectations, not independent human adjudication. This is a product behavior check distinct from article retrieval. Run `OPENAI_MODEL= OPENAI_API_KEY= python -m evals.run_product_eval`.

The first implementation returned irrelevant articles on nine development cases. Article scope checks removed those matches. The challenge set then exposed two compromise reports (C13 and C14) receiving generic recovery guidance; an explicit compromise abstention rule removed those matches. Two development labels were also corrected after review: T38 has relevant approved-version guidance, while T44's generic slowness has no relevant crash guidance. Both sets were authored here, inspected and used during development. They are **not blinded, independent performance estimates**. Exact results should not be extrapolated to real tickets. In particular, keyword rules can miss new compromise phrasing, and relevance of a returned article still needs a human reviewer.

The optional OpenAI draft, actual API cost, latency, deployment, and real-world routing are unmeasured. The [previous GitHub Actions run](https://github.com/kalpanaiitm/enterprise-ai-operations-agen/actions/runs/36456525260) passed before the workflow evaluation was added. Check Actions for the latest commit's CI result.
