# MEDGUIDE AI
## AI-Powered Healthcare Information and Medicine Awareness Assistant

**University Project Report – Generative AI and Large Language Models Elective**

**Student Name:** ____________________  
**Register Number:** ____________________  
**Department:** ____________________  
**Institution:** ____________________  
**Academic Year:** ____________________

---

## 1. Abstract
MedGuide AI is a web-based healthcare information and medicine-awareness assistant developed as an academic demonstration of Generative AI, large language models and retrieval-augmented generation. The application uses Python and Flask for backend services, HTML/CSS/JavaScript for the user interface, a structured JSON/CSV educational knowledge base, TF-IDF vectorization and cosine similarity for retrieval, and Ollama to run the Llama 3.2:3b language model locally. For each supported question, the retrieval module ranks relevant records and supplies up to three records as context to the LLM. The interface displays the response, source links and similarity scores. A retrieval-only fallback keeps the application useful when the local model is unavailable. A simple emergency phrase check runs before LLM generation and returns urgent-care guidance for selected phrases. The system is explicitly educational: it does not diagnose, prescribe medicines, recommend individual dosages or replace professional medical care.

## 2. Introduction
People encounter health information through websites, social media and informal conversations. Such information may be difficult to interpret or may lack reliable references. A conversational interface can make general health-awareness information easier to explore. Generative AI can explain retrieved material in accessible language, while retrieval can ground responses in a curated collection of sources. MedGuide AI combines these techniques in a locally executed academic prototype.

## 3. Problem Statement
A learner or member of the public may need understandable explanations of basic healthcare topics, but unstructured online information can be confusing and an unconstrained language model may generate unsupported statements. The project addresses this educational information problem by retrieving from a small curated knowledge base, displaying source links and applying explicit safety boundaries.

## 4. Objectives
- Build a responsive healthcare-awareness chatbot.
- Integrate a local Llama 3.2 model through Ollama.
- Implement TF-IDF retrieval and cosine similarity.
- Retrieve and display up to three relevant knowledge records.
- Provide source URLs and relevance scores.
- Provide a fallback when Ollama is unavailable.
- Detect selected emergency phrases before generation.
- Collect simple answer helpfulness feedback.
- Demonstrate the complete system through automated tests.

## 5. Existing System
General web search returns many pages and requires users to evaluate relevance and reliability. A standalone language model may answer fluently without grounding its statements in a known source. Static FAQ pages are limited to fixed question-and-answer pairs and do not provide flexible generated explanations.

## 6. Proposed System
MedGuide AI uses a curated educational dataset as its knowledge source. TF-IDF and cosine similarity identify relevant records. The retrieved records are passed to a local LLM as context. The application displays sources and scores so that users can inspect the underlying information. When the model cannot be reached, the system returns retrieved educational text rather than inventing a generated answer.

## 7. Literature and Technology Overview
- **Generative AI:** Models that generate text or other content from learned patterns.
- **LLM:** A large language model capable of understanding prompts and generating natural-language responses.
- **RAG:** Retrieval-augmented generation combines external knowledge retrieval with language generation.
- **TF-IDF:** A statistical representation that gives higher weight to terms important to a document but less common across the corpus.
- **Cosine similarity:** Measures the angle-based similarity between vector representations.
- **Flask:** A lightweight Python web framework.
- **Ollama:** A tool for running supported language models locally.
- **Llama 3.2:3b:** The selected local language model; actual speed depends on hardware.

## 8. System Architecture
The presentation layer contains the HTML page, CSS and JavaScript. Flask handles requests and coordinates the application. The retrieval module loads JSON records and ranks them. The generation component calls the local Ollama API. The architecture and data flow are documented in `architecture.md`.

## 9. Methodology
1. Curate educational question-and-answer records and official source links.
2. Store the records in JSON and CSV.
3. Load JSON records in the retrieval module.
4. Combine topic, question and answer text for each record.
5. Fit a TF-IDF vectorizer to the corpus.
6. Transform each user question using the same vectorizer.
7. Compute cosine similarity and rank records.
8. Select up to three records above a minimum score threshold.
9. Check selected emergency phrases before any LLM call.
10. Construct a constrained prompt from retrieved content and the question.
11. Send the prompt to Ollama and receive a generated response.
12. If generation fails, return a retrieval-based educational fallback.
13. Display the answer and sources in the browser.

## 10. Dataset Description
The starter dataset contains 35 records across hygiene, nutrition, physical activity, sleep, preventive healthcare, vaccination, medicine safety, health terminology, first aid, professional help, mental well-being, food safety and tobacco awareness. Each record includes `id`, `topic`, `question`, `answer` and `source_url`. The JSON file is used by the application; CSV is included for convenient inspection. Sources include WHO, WHO India, Government of India and NHS pages. The dataset is educational and limited in scope; it is not a clinical knowledge system.

## 11. RAG Implementation
`retrieval.py` loads the records and builds a TF-IDF matrix. At question time, the query is transformed into a vector and compared with all document vectors using cosine similarity. The highest-scoring three records are returned with their scores. The scores are text similarity measures, not medical confidence values. Retrieved answer text and URLs are placed in the LLM prompt to ground generation.

## 12. LLM Integration
`app.py` sends a prompt to Ollama's local `/api/generate` endpoint using the configured `llama3.2:3b` model. Streaming is disabled for a simple request-response workflow. The prompt instructs the model to use supplied context, avoid invented citations, avoid individualized medical advice, and direct users to qualified professionals when the context is insufficient. Connection errors result in a retrieval-only fallback.

## 13. Module Descriptions
- `app.py`: Flask routes, validation, emergency check, Ollama integration, fallback and feedback.
- `retrieval.py`: JSON loading, TF-IDF indexing and top-three similarity retrieval.
- `healthcare_knowledge.json`: runtime educational corpus.
- `healthcare_knowledge.csv`: spreadsheet-friendly copy of the corpus.
- `index.html`: page structure.
- `style.css`: responsive blue-and-white interface.
- `script.js`: asynchronous API calls, chat rendering, source display and feedback.
- `test_app.py`: Flask route, validation, emergency and fallback tests.
- `test_retrieval.py`: corpus and retrieval tests.

## 14. Screenshots
**Insert actual screenshots after running the application. Do not use mock screenshots as test evidence.**
1. Home page and disclaimer.
2. A normal question with generated answer.
3. Retrieved sources with cosine similarity scores.
4. Retrieval fallback when Ollama is stopped.
5. Emergency warning response.
6. Test execution output.

## 15. Testing and Results
Automated tests are provided using pytest. They cover the home page, health endpoint, empty question, invalid JSON, emergency bypass, Ollama-unavailable fallback, no-match behavior, feedback endpoint, dataset size and retrieval ranking. Run `python -m pytest -v`. Record the actual pass/fail output, date, Python version and environment in the final submitted report. No test results are claimed in this template.

## 16. Limitations
- The dataset is small and does not cover all health topics.
- TF-IDF is lexical retrieval and may miss semantically related wording.
- Similarity scores do not measure correctness or clinical relevance.
- Emergency phrase matching is not comprehensive and is not a triage system.
- LLM output can still be inaccurate despite prompt constraints.
- Local model speed and availability depend on hardware and installation.
- The project does not authenticate users or persist feedback.
- Source pages and guidance can change; links should be reviewed periodically.

## 17. Future Enhancements
- Expand and medically review the knowledge base.
- Add semantic embeddings and a vector database.
- Add source versioning and scheduled source review.
- Add multilingual support after safety evaluation.
- Improve emergency handling with carefully validated rules and usability testing.
- Add privacy-preserving analytics and persistent feedback with consent.
- Conduct expert review, bias evaluation and usability testing before any public deployment.

## 18. Conclusion
MedGuide AI demonstrates a complete educational RAG workflow using Flask, TF-IDF, cosine similarity, Ollama and Llama 3.2:3b. It retrieves relevant knowledge records, provides grounded context to a local LLM, displays source information and includes fallback and emergency safeguards. The prototype is suitable for academic demonstration, but not for clinical use or personal medical decision-making.

## 19. References
1. World Health Organization, Healthy Diet: https://www.who.int/news-room/fact-sheets/detail/healthy-diet
2. World Health Organization, Infection Prevention and Control in India: https://www.who.int/india/health-topics/infection-prevention-and-control
3. World Health Organization, Vaccines and Immunization: https://www.who.int/health-topics/vaccines-and-immunization
4. World Health Organization, Antimicrobial Resistance in India: https://www.who.int/india/health-topics/antimicrobial-resistance
5. World Health Organization, WASH and Health: https://www.who.int/tools/compendium-on-health-and-environment/wash
6. NHS, First Aid: https://www.nhs.uk/conditions/first-aid/
7. Ollama Documentation: https://ollama.com/
8. Flask Documentation: https://flask.palletsprojects.com/
9. scikit-learn Documentation: https://scikit-learn.org/stable/
10. Python Documentation: https://docs.python.org/3/
