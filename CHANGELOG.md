# Changelog

## 2026-09-28 — Original fictional IT support MVP

Implemented a LangGraph ticket flow, three original fictional support articles, TF-IDF retrieval, optional model drafting, a checkpointed human-review interrupt, FastAPI endpoints, tests, and explicit scope documentation. This project does not contain coursework or capstone assets.

## 2026-09-28 — Fixed baseline evaluation

Added four fictional cases for deterministic category and retrieval expectations, with a CI evaluation command. The model-backed drafting path remains outside this baseline.

## 2026-09-28 — Model boundary checks

Added mocked model success, unsafe output, sensitive-ticket bypass, and provider-failure tests. Restricted cited IDs to retrieved articles and bounded optional calls to 250 output tokens, with no automatic retries or response storage. The model quality and actual API cost remain unmeasured.

## 2026-09-28 — Expanded fictional evaluation

Added 60 authored fictional tickets, three narrowly scoped articles for Wi-Fi, MFA, and app crashes, category phrase and word-boundary checks, separate evidence-hit and abstention measures, sensitive-flag recall, and a CI regression floor. Reported nine false article matches instead of treating lexical overlap as validated relevance. No coursework material is used.

## 2026-09-28 — Relevance and incident triage refinement

Added article-specific scope checks so broad lexical overlap does not automatically become evidence. Compromise reports now abstain from generic recovery articles and remain behind human review. Added 16 further fictional challenge tickets, including security negatives, and documented the fact that both authored sets were inspected during development.
