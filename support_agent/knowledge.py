"""Search only the small, original fictional knowledge base."""
import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = json.loads((Path(__file__).resolve().parent.parent / "data" / "knowledge.json").read_text())
VECTORIZER = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
VECTORS = VECTORIZER.fit_transform([doc["title"] + " " + doc["text"] for doc in DOCS])

# Each article has a narrow scope. Lexical similarity alone can match a broad
# request to guidance that does not actually address the request.
SCOPE = {
    "KB-NETWORK-01": ("vpn", "tunnel", "vpn status"),
    "KB-NETWORK-02": ("wi-fi", "wifi", "wireless", "internet"),
    "KB-ACCOUNT-01": ("account", "password", "login", "credentials", "recovery"),
    "KB-ACCOUNT-02": ("mfa", "one-time code", "verification code"),
    "KB-SOFTWARE-01": ("update", "updating", "version", "catalogue", "installation", "install"),
    "KB-SOFTWARE-02": ("crash", "crashes", "freeze", "freezes", "launch"),
}


def _in_scope(query: str, doc_id: str) -> bool:
    text = query.lower()
    if doc_id == "KB-SOFTWARE-01" and re.search(r"\b(?:outside|unapproved)\b", text):
        return False
    return any(re.search(r"\b" + re.escape(term) + r"\b", text)
               for term in SCOPE[doc_id])


def search(query: str, category: str, limit: int = 2) -> list[dict]:
    """Return positive-scoring passages; never present a zero-score document as evidence."""
    # A report of compromise needs incident triage, which none of these
    # fictional articles cover. Keep unrelated recovery advice out of drafts.
    if re.search(r"\b(?:stolen|leaked|phishing|breach|compromised)\b", query, re.IGNORECASE):
        return []
    scores = cosine_similarity(VECTORIZER.transform([query]), VECTORS).ravel()
    ranked = sorted(
        ((float(scores[i]), doc) for i, doc in enumerate(DOCS)
         if doc["category"] == category and _in_scope(query, doc["id"])),
        key=lambda pair: pair[0],
        reverse=True,
    )
    return [
        {"id": doc["id"], "title": doc["title"], "text": doc["text"], "score": round(score, 3)}
        for score, doc in ranked[:limit] if score > 0
    ]
