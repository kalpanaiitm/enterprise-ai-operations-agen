"""Small fixed, deterministic baseline evaluation. No LLM or external data."""
import json
from pathlib import Path

from support_agent.knowledge import search
from support_agent.workflow import classify


def run() -> dict:
    cases = json.loads((Path(__file__).parent / "cases.json").read_text())
    category_correct = 0
    retrieval_correct = 0
    retrieval_total = 0
    rows = []
    for case in cases:
        actual_category = classify({"ticket": case["ticket"]})["category"]
        docs = search(case["ticket"], actual_category) if actual_category != "unknown" else []
        found = [doc["id"] for doc in docs]
        category_ok = actual_category == case["category"]
        retrieval_ok = case["expected_id"] in found if case["expected_id"] else not found
        category_correct += category_ok
        retrieval_correct += retrieval_ok
        retrieval_total += 1
        rows.append({"category_ok": category_ok, "retrieval_ok": retrieval_ok})
    return {"cases": len(cases), "category_correct": category_correct,
            "retrieval_correct": retrieval_correct, "rows": rows}


if __name__ == "__main__":
    result = run()
    print(f'Category: {result["category_correct"]}/{result["cases"]}')
    print(f'Retrieval expectation: {result["retrieval_correct"]}/{result["cases"]}')
    raise SystemExit(0 if all(row["category_ok"] and row["retrieval_ok"] for row in result["rows"]) else 1)
