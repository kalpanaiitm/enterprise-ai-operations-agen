# Test report

## Local verification — 2026-09-28

`python -m pytest -q`: **10 passed**. `python -m evals.run_eval` on 60 original fictional tickets:

| Measure | Result |
| --- | ---: |
| Category accuracy | 60/60 |
| Expected article present, where one applies | 34/34 |
| No article returned, where none applies | 17/26 |
| Sensitive ticket detection recall | 10/10 |

The nine false article matches are T04, T07, T09, T15, T25, T26, T35, T38, and T43. They include broad network, account, and software requests that share words with an article but are not addressed by its instructions. Retrieval currently accepts any positive TF-IDF score, and does not reliably abstain on such queries. The case labels and six articles are fictional, authored for this repository; these are in-sample checks and not real-world performance estimates. The optional OpenAI draft, actual API cost, latency, and production deployment are unmeasured. A human must decide whether any retrieved article applies.

A prior four-case smoke evaluation and [GitHub Actions run](https://github.com/kalpanaiitm/enterprise-ai-operations-agen/actions/runs/36454190246) passed before this expansion. The expanded evaluation's CI status should be checked on the current commit.
