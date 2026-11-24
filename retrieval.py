"""TF-IDF based retrieval for MedGuide AI."""
from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = Path(__file__).parent / "data" / "healthcare_knowledge.json"

class KnowledgeRetriever:
    def __init__(self, data_path=DATA_PATH):
        self.data_path = Path(data_path)
        self.records = self._load_records()
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.documents = [
            f"{r['topic']} {r['question']} {r['answer']}" for r in self.records
        ]
        self.matrix = self.vectorizer.fit_transform(self.documents) if self.documents else None

    def _load_records(self):
        if not self.data_path.exists():
            return []
        payload = json.loads(self.data_path.read_text(encoding="utf-8"))
        records = payload.get("records", [])
        required = {"id", "topic", "question", "answer", "source_url"}
        for item in records:
            if not required.issubset(item):
                raise ValueError("A knowledge record is missing required fields.")
        return records

    def retrieve(self, query, top_k=3, min_score=0.01):
        """Return up to top_k records with cosine relevance scores (0..1)."""
        if not query or not query.strip() or self.matrix is None:
            return []
        query_vector = self.vectorizer.transform([query.strip()])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        ranked = sorted(enumerate(scores), key=lambda pair: pair[1], reverse=True)
        results = []
        for index, score in ranked[:max(1, top_k)]:
            if float(score) < min_score:
                continue
            item = dict(self.records[index])
            item["score"] = round(float(score), 4)
            results.append(item)
        return results
