"""Search only the small, original fictional knowledge base."""
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = json.loads((Path(__file__).resolve().parent.parent / "data" / "knowledge.json").read_text())
VECTORIZER = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
VECTORS = VECTORIZER.fit_transform([doc["title"] + " " + doc["text"] for doc in DOCS])


def search(query: str, category: str, limit: int = 2) -> list[dict]:
    """Return positive-scoring passages; never present a zero-score document as evidence."""
    scores = cosine_similarity(VECTORIZER.transform([query]), VECTORS).ravel()
    ranked = sorted(
        ((float(scores[i]), doc) for i, doc in enumerate(DOCS) if doc["category"] == category),
        key=lambda pair: pair[0],
        reverse=True,
    )
    return [
        {"id": doc["id"], "title": doc["title"], "text": doc["text"], "score": round(score, 3)}
        for score, doc in ranked[:limit] if score > 0
    ]
