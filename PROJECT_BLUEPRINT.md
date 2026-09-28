# Project blueprint

## Problem and user
A support specialist needs a traceable way to find relevant internal guidance and prepare a reply without automatically sending unsafe advice. The primary user is a human reviewer of fictional IT tickets.

## MVP contract
Input: 10–2,000 characters of fictional ticket text. Output: category, retrieved original article IDs and scores, draft, audit steps, and a pending human-review state. A separate review decision approves, edits, or rejects; there is no outbound action.

## Build versus reuse
LangGraph supplies checkpointed state and interrupt/resume. scikit-learn supplies a transparent TF-IDF baseline. FastAPI supplies validation and local API docs. A custom multi-agent hierarchy is unnecessary for this bounded workflow.

## Ground truth
Only `data/knowledge.json` is eligible retrieval evidence. Its articles are fictional; their content is not real corporate policy. Unknown queries have an explicit no-evidence path.

## Guardrails and cost
Ticket content is data, not a tool command. No secrets in the repo. Model calls are disabled by default; optional draft generation costs at most one configured OpenAI call per non-sensitive ticket with evidence, capped at 250 output tokens. There is no monthly spend control. All outcomes require human review. The process stores checkpoints only in memory; logs should avoid ticket text.

## Acceptance
A related ticket returns a source ID; an unrelated ticket returns no evidence; sensitive tickets are flagged; every ticket pauses; review resumes once; a second review is rejected; no message is sent. CI must pass before claiming verification.

## Out of scope
Real enterprise systems, external integrations, durable persistence, authentication, production deployment, and autonomous ticket resolution.
