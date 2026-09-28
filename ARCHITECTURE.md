# Architecture

```text
FastAPI ticket → classify → scoped TF-IDF retrieval → draft → LangGraph interrupt
                                     ↓                         ↓
                        fictional local articles      human approve/edit/reject
```

`support_agent/knowledge.py` owns the immutable corpus and scores. `workflow.py` owns typed graph state, optional model draft, checkpointed interrupt and review status. `api.py` validates inputs and resumes the graph using the same thread ID. The API returns drafts but has no send endpoint or external side-effect tool.

The model is optional. The graph still runs and pauses with deterministic drafting when no model is configured. Sensitive tickets bypass the model. A response with no allowed citation, an unknown citation, or selected unsafe phrases falls back to deterministic drafting, as does a provider failure. These narrow checks do not certify factual accuracy. `InMemorySaver` is a local demonstration checkpoint and is lost on process restart. No PII or coursework data belongs in examples.
