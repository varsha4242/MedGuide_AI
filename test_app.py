import app as app_module

def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()

def test_home_page():
    response = client().get("/")
    assert response.status_code == 200
    assert b"MedGuide AI" in response.data

def test_health_endpoint():
    response = client().get("/api/health")
    data = response.get_json()
    assert response.status_code == 200
    assert data["dataset_records"] >= 30
    assert data["model"] == "llama3.2:3b"

def test_empty_question():
    response = client().post("/api/ask", json={"question": "  "})
    assert response.status_code == 400

def test_invalid_json():
    response = client().post("/api/ask", data="{bad", content_type="application/json")
    assert response.status_code == 400

def test_emergency_bypasses_ollama(monkeypatch):
    def should_not_run(*args, **kwargs):
        raise AssertionError("LLM must not run for emergency input")
    monkeypatch.setattr(app_module, "generate_with_ollama", should_not_run)
    response = client().post("/api/ask", json={"question": "I have severe chest pain"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["emergency"] is True
    assert data["mode"] == "emergency"

def test_ollama_unavailable_fallback(monkeypatch):
    def fail(*args, **kwargs):
        raise app_module.requests.ConnectionError("Ollama offline")
    monkeypatch.setattr(app_module, "generate_with_ollama", fail)
    response = client().post("/api/ask", json={"question": "Why is handwashing important?"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["mode"] == "retrieval_fallback"
    assert len(data["sources"]) > 0
    assert "educational" in data["answer"].lower()

def test_no_matching_records():
    response = client().post("/api/ask", json={"question": "quantum spacecraft propulsion"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["mode"] == "knowledge_base_no_match"
    assert data["sources"] == []

def test_feedback_endpoint():
    response = client().post("/api/feedback", json={"helpful": True})
    assert response.status_code == 200
    assert response.get_json()["received"] is True
