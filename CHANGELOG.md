# Changelog

## 2026-09-28 — Original fictional IT support MVP

Implemented a LangGraph ticket flow, three original fictional support articles, TF-IDF retrieval, optional model drafting, a checkpointed human-review interrupt, FastAPI endpoints, tests, and explicit scope documentation. This project does not contain coursework or capstone assets.

## 2026-09-28 — Fixed baseline evaluation

Added four fictional cases for deterministic category and retrieval expectations, with a CI evaluation command. The model-backed drafting path remains outside this baseline.

## 2026-09-28 — Model boundary checks

Added mocked model success, unsafe output, sensitive-ticket bypass, and provider-failure tests. Restricted cited IDs to retrieved articles and bounded optional calls to 250 output tokens, with no automatic retries or response storage. The model quality and actual API cost remain unmeasured.
