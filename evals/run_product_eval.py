"""Offline workflow eval: authored escalation and draft expectations, no API key."""
import json
import os
import re
from pathlib import Path

from support_agent.workflow import create_graph


def run() -> dict:
    if os.getenv("OPENAI_MODEL") or os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Unset OPENAI_MODEL and OPENAI_API_KEY for the offline product eval")
    cases = json.loads((Path(__file__).parent / "product_cases.json").read_text())
    graph = create_graph()
    rows = []
    for case in cases:
        state = graph.invoke({"ticket": case["ticket"]},
                             {"configurable": {"thread_id": "product-" + case["id"]}})
        pause = state.get("__interrupt__", ())
        decision = pause[0].value if pause else {}
        source = case["source"]
        ids = {doc["id"] for doc in state["evidence"]}
        citations = set(re.findall(r"\[(KB-[A-Z]+-\d+)\]", state["draft"]))
        rows.append({
            "id": case["id"],
            "escalation_ok": decision.get("needs_escalation") == case["escalate"],
            "source_ok": (source in ids if source else not ids),
            "draft_ok": (case["draft_contains"] in state["draft"] and
                         (citations == {source} if source else not citations) and
                         not re.search(r"\b(?:we|I) (?:have )?(?:fixed|resolved|installed)\b",
                                       state["draft"], re.IGNORECASE)),
            "review_paused": bool(pause) and graph.get_state(
                {"configurable": {"thread_id": "product-" + case["id"]}}).next == ("review",),
            "model_disabled": state["model_used"] == "deterministic",
        })
    return {"cases": len(rows), "rows": rows,
            **{key: sum(row[key] for row in rows) for key in
               ("escalation_ok", "source_ok", "draft_ok", "review_paused", "model_disabled")}}


if __name__ == "__main__":
    result = run()
    for key in ("escalation_ok", "source_ok", "draft_ok", "review_paused", "model_disabled"):
        print(f"{key}: {result[key]}/{result['cases']}")
    print("Failures:", ", ".join(row["id"] for row in result["rows"]
                               if not all(value for key, value in row.items() if key != "id")) or "none")
