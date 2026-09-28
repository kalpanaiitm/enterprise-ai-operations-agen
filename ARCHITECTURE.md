# Architecture

```text
FastAPI ticket → classify → scoped TF-IDF retrieval → draft → LangGraph interrupt
                                     ↓                         ↓
                        fictional local articles      human approve/edit/reject
```

`support_agent/knowledge.py` owns the immutable corpus and scores. `workflow.py` owns typed graph state, optional model draft, checkpointed interrupt and review status. `api.py` validates inputs and resumes the graph using the same thread ID. The API returns drafts but has no send endpoint or external side-effect tool.

The model is optional. The graph still runs and pauses with deterministic drafting when no model is configured. Failure of a model call falls back to deterministic drafting; this does not certify the answer as accurate. `InMemorySaver` is a local demonstration checkpoint and is lost on process restart. No PII or coursework data belongs in examples.
