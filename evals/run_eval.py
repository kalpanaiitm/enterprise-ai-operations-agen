"""Deterministic evaluation on original fictional tickets; no external model call."""
import json
from collections import defaultdict
from pathlib import Path

from support_agent.knowledge import search
from support_agent.workflow import classify


def run() -> dict:
    cases = json.loads((Path(__file__).parent / "cases.json").read_text())
    rows = []
    by_tag = defaultdict(lambda: {"count": 0, "category_correct": 0, "evidence_correct": 0})
    for case in cases:
        classification = classify({"ticket": case["ticket"]})
        category = classification["category"]
        found = [doc["id"] for doc in search(case["ticket"], category)] if category != "unknown" else []
        expected = case["expected_id"]
        category_ok = category == case["category"]
        evidence_ok = expected in found if expected else not found
        row = {"id": case["id"], "tag": case["tag"], "category": category,
               "expected_category": case["category"], "found_ids": found,
               "expected_id": expected, "category_ok": category_ok,
               "evidence_ok": evidence_ok, "sensitive_ok": not case["sensitive"] or classification["sensitive"]}
        rows.append(row)
        group = by_tag[case["tag"]]
        group["count"] += 1
        group["category_correct"] += category_ok
        group["evidence_correct"] += evidence_ok
    relevant = [row for row in rows if row["expected_id"]]
    abstain = [row for row in rows if not row["expected_id"]]
    sensitive = [row for row, case in zip(rows, cases) if case["sensitive"]]
    return {
        "cases": len(rows), "category_correct": sum(row["category_ok"] for row in rows),
        "retrieval_correct": sum(row["evidence_ok"] for row in rows),
        "evidence_hits": sum(row["evidence_ok"] for row in relevant),
        "evidence_cases": len(relevant),
        "abstentions": sum(row["evidence_ok"] for row in abstain),
        "abstention_cases": len(abstain),
        "sensitive_detected": sum(row["sensitive_ok"] for row in sensitive),
        "sensitive_cases": len(sensitive),
        "by_tag": dict(by_tag), "rows": rows,
    }


if __name__ == "__main__":
    result = run()
    for label, numerator, denominator in (
        ("Category", result["category_correct"], result["cases"]),
        ("Evidence hit", result["evidence_hits"], result["evidence_cases"]),
        ("Abstention", result["abstentions"], result["abstention_cases"]),
        ("Sensitive flag recall", result["sensitive_detected"], result["sensitive_cases"]),
    ):
        print(f"{label}: {numerator}/{denominator}")
    print("Failures:", ", ".join(row["id"] for row in result["rows"]
                               if not row["category_ok"] or not row["evidence_ok"] or not row["sensitive_ok"]) or "none")
