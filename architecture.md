# MedGuide AI – Architecture and Data Flow

## Architecture
1. **Presentation layer:** `templates/index.html`, `static/css/style.css` and `static/js/script.js` provide the responsive browser interface.
2. **Application layer:** `app.py` exposes Flask routes, validates input, detects emergency phrases, coordinates retrieval and generation, and returns JSON.
3. **Retrieval layer:** `retrieval.py` loads the JSON knowledge base, converts each record into a TF-IDF vector and ranks records using cosine similarity.
4. **Knowledge layer:** JSON is the runtime source of truth; CSV is supplied for inspection and spreadsheet analysis.
5. **Generation layer:** Ollama's local HTTP API runs `llama3.2:3b`. The prompt contains the question and retrieved context and constrains the model to educational answers.

## Data flow
- Browser submits `{ "question": "..." }` to `POST /api/ask`.
- Flask validates the request and checks emergency phrases first.
- Emergency match: return emergency guidance immediately; do not call retrieval or Ollama.
- Otherwise, TF-IDF transforms the question and cosine similarity ranks the corpus.
- Up to three records above the minimum similarity threshold are returned.
- No match: return a transparent no-match response.
- Match: send the retrieved answers and source URLs to Ollama.
- Ollama success: return generated answer, `ollama_rag` mode and sources.
- Ollama error: return the retrieved educational content as `retrieval_fallback`.
- Browser renders answer, source links and scores; feedback is posted to `/api/feedback`.

## Retrieval mathematics
For query vector q and document vector d, cosine similarity is:

`cos(q,d) = (q · d) / (||q|| ||d||)`

TF-IDF weights terms according to their frequency in a document and rarity across the corpus. Scores are similarity indicators, not clinical confidence or factual validation.

## API
- `GET /`: render chatbot page.
- `GET /api/health`: return service status, record count and model name.
- `POST /api/ask`: accept JSON `{ "question": "..." }`.
- `POST /api/feedback`: accept JSON `{ "helpful": true }` or false.

## Safety and privacy boundaries
- Emergency phrase matching is deliberately simple and may miss emergencies or flag non-emergencies. It is not a triage tool.
- Emergency responses advise immediate contact with emergency services; generation is bypassed.
- No personal health profile is stored. Feedback is kept in memory only and disappears on restart.
- Do not enter identifiable or sensitive health information into this academic demo.
- No external LLM API is used; Ollama runs locally.
