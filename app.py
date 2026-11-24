"""Flask application for MedGuide AI. Educational use only."""
from pathlib import Path
import json
import os
import re
import requests
from flask import Flask, jsonify, render_template, request
from retrieval import KnowledgeRetriever

BASE_DIR = Path(__file__).parent
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "45"))

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
retriever = KnowledgeRetriever()
feedback_log = []

DISCLAIMER = (
    "MedGuide AI provides general educational information only. It does not "
    "diagnose conditions, prescribe or recommend medicines or dosages, or replace "
    "a qualified healthcare professional."
)

# Conservative phrase matching. This is a safety prompt, not a clinical triage system.
EMERGENCY_PATTERNS = [
    r"\b(chest pain|crushing chest pain|severe chest pain)\b",
    r"\b(can't breathe|cannot breathe|difficulty breathing|severe shortness of breath)\b",
    r"\b(unconscious|not responding|unresponsive)\b",
    r"\b(stroke symptoms|face drooping|one side weakness|slurred speech)\b",
    r"\b(severe bleeding|bleeding won't stop|uncontrolled bleeding)\b",
    r"\b(seizure|convulsion)\b",
    r"\b(overdose|poisoning|swallowed poison)\b",
]
EMERGENCY_MESSAGE = (
    "EMERGENCY WARNING: The symptoms described may require immediate medical attention. "
    "Call India's emergency number 112 or your local emergency services now, or go to the "
    "nearest emergency department. Do not wait for this chatbot or an AI-generated answer. "
    "Follow the emergency operator's instructions."
)

def is_emergency(question):
    text = (question or "").lower()
    return any(re.search(pattern, text) for pattern in EMERGENCY_PATTERNS)

def safe_fallback(sources):
    if not sources:
        return (
            "I could not find a sufficiently relevant entry in the educational knowledge "
            "base. Please consult a qualified healthcare professional or an official health "
            "authority. I cannot provide a diagnosis or individualized treatment advice."
        )
    parts = ["Here is general educational information from the MedGuide AI knowledge base:"]
    for source in sources:
        parts.append(f"- {source['answer']}")
    parts.append(
        "This is general information, not a diagnosis or treatment plan. Please consult "
        "a qualified healthcare professional for advice about an individual situation."
    )
    return "\n\n".join(parts)

def generate_with_ollama(question, sources):
    context = "\n\n".join(
        f"Source {i+1} ({s['topic']}): {s['answer']} URL: {s['source_url']}"
        for i, s in enumerate(sources)
    )
    prompt = f"""You are MedGuide AI, a cautious healthcare education assistant.
Answer only general health-awareness questions. Use only the supplied context.
If the context does not answer the question, say so and direct the user to a qualified
healthcare professional or official health authority. Do not diagnose, prescribe, suggest
a medicine for an individual, calculate or recommend dosage, or replace professional care.
Do not invent facts, citations, or source URLs. Use plain, accessible language.
If asked for personalized medical advice, politely decline and recommend a qualified
healthcare professional.

KNOWLEDGE BASE CONTEXT:
{context}

USER QUESTION:
{question}

Give a concise educational answer and mention that it is not medical advice."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=OLLAMA_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    answer = payload.get("response", "").strip()
    if not answer:
        raise ValueError("Ollama returned an empty response.")
    return answer

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "dataset_records": len(retriever.records),
        "model": MODEL_NAME,
        "ollama_endpoint": OLLAMA_URL,
        "disclaimer": DISCLAIMER
    })

@app.post("/api/ask")
def ask():
    if not request.is_json:
        return jsonify({"error": "Please send a JSON request with a question."}), 400
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid JSON body. Send an object containing question."}), 400
    question = payload.get("question", "")
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "Please enter a question before asking."}), 400
    question = question.strip()[:1500]

    # Emergency guidance is returned before retrieval or any LLM network request.
    if is_emergency(question):
        return jsonify({
            "answer": EMERGENCY_MESSAGE,
            "mode": "emergency",
            "emergency": True,
            "sources": [],
            "disclaimer": DISCLAIMER
        })

    sources = retriever.retrieve(question, top_k=3)
    if not sources:
        return jsonify({
            "answer": safe_fallback([]),
            "mode": "knowledge_base_no_match",
            "emergency": False,
            "sources": [],
            "disclaimer": DISCLAIMER
        })

    try:
        answer = generate_with_ollama(question, sources)
        mode = "ollama_rag"
    except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError):
        answer = safe_fallback(sources)
        mode = "retrieval_fallback"

    return jsonify({
        "answer": answer,
        "mode": mode,
        "emergency": False,
        "sources": sources,
        "disclaimer": DISCLAIMER
    })

@app.post("/api/feedback")
def feedback():
    if not request.is_json:
        return jsonify({"error": "Please send feedback as JSON."}), 400
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid JSON body."}), 400
    helpful = payload.get("helpful")
    if not isinstance(helpful, bool):
        return jsonify({"error": "The helpful field must be true or false."}), 400
    # In-memory demo log; feedback is not persisted after app restart.
    feedback_log.append({"helpful": helpful})
    return jsonify({"message": "Thank you for your feedback.", "received": True}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
