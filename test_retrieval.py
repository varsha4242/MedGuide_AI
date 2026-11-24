from retrieval import KnowledgeRetriever

def test_dataset_has_at_least_30_records():
    retriever = KnowledgeRetriever()
    assert len(retriever.records) >= 30

def test_retrieval_returns_up_to_three_relevant_records():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve("Why is handwashing important?", top_k=3)
    assert 1 <= len(results) <= 3
    assert all("score" in item and 0 <= item["score"] <= 1 for item in results)
    assert "hygiene" in results[0]["topic"]

def test_no_match_returns_empty_list():
    retriever = KnowledgeRetriever()
    assert retriever.retrieve("quantum spacecraft propulsion", top_k=3) == []
