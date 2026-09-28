# IT Support Operations Agent — fictional portfolio demo

A small **LangGraph support-ticket workflow** with scoped retrieval, an optional OpenAI draft, and a mandatory human review interrupt. All tickets and knowledge articles in the examples are fictional and original to this repository. This is independent of coursework.

## What is implemented

1. Accept a fictional ticket through FastAPI.
2. Classify account, network, software, or unknown issues with deterministic rules.
3. Retrieve matching articles from a six-document local TF-IDF knowledge base. Zero-score and out-of-scope articles are excluded; compromise reports receive no generic article.
4. Draft a suggested answer. By default this is a deterministic, source-linked template. If both `OPENAI_MODEL` and `OPENAI_API_KEY` are set, the OpenAI Responses API is used for one draft call on a non-sensitive ticket with evidence. The call has a 250-token output limit and no retries or response storage. Missing or unknown citations, selected unsafe language, or API failure fall back to the template.
5. Pause at a LangGraph `interrupt()` for a human to approve, edit, or reject. The API **never sends** the response to anyone.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn support_agent.api:app --host 127.0.0.1 --port 8000
python -m pytest -q
```

Open http://127.0.0.1:8000/docs and submit a ticket such as `My VPN connection is failing`. The POST returns a `ticket_id` and `pending_review`; use `POST /tickets/{ticket_id}/review` with `{"approved":true,"edited_response":"Reviewed guidance."}` to resume. `GET /tickets/{ticket_id}` displays the current state.

The 60-case development set is in `evals/cases.json`; a separate 16-case challenge set is in `evals/challenge_cases.json`. Run `python -m evals.run_eval` and `python -m evals.run_eval --cases evals/challenge_cases.json` for category, evidence-hit, abstention, and sensitive-flag results. See `TEST_REPORT.md` for measured counts and limits. The default runs without an API key. For an **optional paid model call**, set `OPENAI_MODEL` to a model available in your account and `OPENAI_API_KEY` locally. Never commit a key. Use synthetic tickets only. Sensitive tickets skip the external model and require review. There is no monthly spend cap in this app; leave the model disabled unless you intend to pay for calls.

## Engineering evidence and limits

See [discovery brief](DISCOVERY_BRIEF.md), [blueprint](PROJECT_BLUEPRINT.md), [architecture](ARCHITECTURE.md), [tests](TEST_REPORT.md), [demo walkthrough](DEMO_WALKTHROUGH.md), and [changelog](CHANGELOG.md). The in-memory checkpoint is lost on restart; this local demo has no authentication, durable audit store, production monitoring, or delivery integration. Article-specific scope checks improve abstention on the authored cases; a lexical match is still not proof that an article applies to a new request. Rule classification can miss untested phrasing. The citation and phrase checks are narrow; they do **not** prove full grounding or safety. A human must verify every draft, especially sensitive tickets. Do not deploy this demo as a public support service.
